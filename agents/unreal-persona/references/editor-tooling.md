---
name: editor-tooling
metadata:
  version: "1.1"
---

# Editor Tooling

## Use This Reference When
- Building or extending custom editor tools: details panel customizations, asset validators, commandlets, or utility widgets
- Diagnosing crashes on editor module reload, shutdown, or hot reload caused by stale registered callbacks or vtable pointers
- Deciding which editor extension mechanism is appropriate for a given tool (EUW vs IDetailCustomization vs Commandlet vs Scripted Action)
- Authoring batch content processing tools that must run headlessly in CI or as part of a cook pipeline

## Veteran Expert Stance
Editor extension in Unreal is a layered system: Blueprint-accessible Editor Utility Widgets at the top for designer-facing tools, C++ IDetailCustomization and IPropertyTypeCustomization for precise inspector control, and Commandlets at the bottom for fully headless automation. Choosing the wrong layer wastes time — a tool that needs structured UI and asset iteration should not be a Commandlet, and a Commandlet that needs to run in CI without a display should not be an EUW. Map the tool's operator and environment to the correct mechanism before writing a line of code.

Registration and unregistration symmetry is not optional. Every detail customization, asset type action, and asset validator registered in StartupModule() must have a matching unregistration in ShutdownModule(). Forgetting this is the single most common cause of crashes on live-coding hot reload and module unload: the engine still holds a delegate or function pointer into a DLL whose memory has been unmapped. These crashes manifest as access violations in unrelated editor systems, making them appear to be engine bugs when they are module lifecycle bugs.

Editor code that calls into game runtime types must respect the module dependency direction. Editor modules depend on Runtime modules; Runtime modules must not depend on Editor modules. The moment an editor-only type (any type from an Editor-only module) appears in a Runtime module's header without a WITH_EDITOR guard, you have a shipping build link error waiting to surface on the first platform cook. Treat this boundary as strictly as you would treat a public API boundary.

## Core Concerns
- Editor module lifecycle (StartupModule / ShutdownModule) governs registration and unregistration of all editor extension objects; unregistration failures cause deferred crashes that are hard to attribute
- IDetailCustomization and IPropertyTypeCustomization are the correct C++ mechanisms for inspector-level control; EUW is the correct mechanism for designer-facing operational tools
- Commandlets are the correct mechanism for headless batch processing; they run with full editor context but no display server, making them suitable for CI pipelines
- UEditorValidatorBase provides a structured hook into the content validation system; ad-hoc asset checking in editor code is not integrated into the engine's validation reporting
- All editor types and editor module APIs are stripped from shipping builds; any runtime code path that touches them requires WITH_EDITOR guards or a module type boundary
- FSlateApplication and editor notification APIs are only valid in editor context; commandlets and runtime code must not call them unconditionally

## Practical Heuristics

1. Register IDetailCustomization in StartupModule() using FPropertyEditorModule::RegisterCustomClassLayout(ClassName, Delegate). The ClassName must match exactly the class name as a FName, without the U/A prefix. Always store the registered name and call UnregisterCustomClassLayout() in ShutdownModule() with the same name.

2. IPropertyTypeCustomization is more granular than IDetailCustomization — it customizes how a USTRUCT appears in any details panel that contains it, regardless of the owning class. Use this when the same struct appears across many UObjects and needs consistent display everywhere.

3. CreateDetailLayout() in IDetailCustomization receives an IDetailLayoutBuilder&. Call HideProperty() before adding custom rows to prevent the default property widget from appearing alongside your custom one. Forgetting HideProperty() results in duplicate entries.

4. Editor Utility Widgets (EUWs) are the right tool for artist/designer-facing operational tools — batch renaming, material swapping, LOD validation with visual feedback. They run in the editor process with full Blueprint API access and are registered simply by right-clicking in the Content Browser. Use them when the operator is not a programmer and the tool needs a UI.

5. Editor Utility Blueprints (UEditorUtilityObject subclasses) are the right tool for non-UI batch operations that designers need to trigger: "process all assets in this folder," "validate naming conventions." They appear in the right-click menu of selected assets via Blutility and require no C++ UI code.

6. Scripted Actions (Editor Utility Blueprints with GetSupportedClass() implemented) surface as right-click context menu entries on specific asset types in the Content Browser. Use them for per-asset operations that are too specialized for a global commandlet but too frequent to require a full Blutility UI.

7. Commandlets run as: `UnrealEditor-Cmd.exe ProjectName -run=MyCommandlet [args]`. They have full UObject system access, can iterate the asset registry, load packages, and modify assets — all without a display. This makes them the correct choice for CI validation, automated content migration, and cook-pipeline preprocessing. They do not require -game or -editor flags; -run= implies editor context.

8. In a Commandlet, GIsEditor is true and GIsRunningCommandlet is true. Never call FSlateApplication::Get() or any display-dependent API inside a Commandlet without checking IsRunningCommandlet(). Use UE_LOG for output; it is captured by the CI log without needing a display.

9. UEditorValidatorBase::ValidateAsset() should call AssetFails(Asset, FText) to register failure messages through the engine's validation result system. Do not use UE_LOG alone — log output is not captured by the Content Validation UI or the automated validation pipeline. Both are appropriate together.

10. Register UEditorValidatorBase subclasses via UEditorValidatorSubsystem::AddValidator(). They run automatically during Content Validation (Editor → Tools → Validate Content) and can be wired to run on save via project settings. The subsystem handles iteration; validators should be stateless.

11. FAssetTypeActions_Base lets you add right-click actions and control the asset color and category in the Content Browser for a custom UObject-derived asset type. Register with FAssetToolsModule::RegisterAssetTypeActions() in StartupModule and unregister in ShutdownModule using the returned TSharedRef handle.

12. When displaying editor notifications (toast messages at the top of the viewport), use FNotificationInfo with FSlateNotificationManager::Get().AddNotification(). Only call this from the game thread. For commandlets and background operations, prefer UE_LOG or writing a result file.

13. IDetailCategoryBuilder::AddCustomRow() lets you insert a completely custom widget row into a details category. The row takes a FDetailWidgetRow that accepts a NameContent and a ValueContent widget. Use SHorizontalBox with inline buttons for operation triggers — this pattern is common for "Validate" or "Reset to Default" buttons in a details panel.

14. TSharedRef<IDetailCustomization> Create() factory functions should not capture heavy state. The lifetime of a customization object is tied to the details panel's lifetime, which closes when the selection changes. Store minimal state; query the object being inspected through IDetailLayoutBuilder::GetSelectedObjects() each time the panel rebuilds.

15. With live coding enabled, editor module reload goes through a module unload/reload sequence. Anything that captures a raw function pointer or stores a raw C++ vtable pointer to objects allocated in the old DLL segment will crash on the next use. Use FDelegateHandle (returned by AddUObject, AddRaw, etc.) to store and remove delegate bindings, not raw pointer comparisons.

16. GEngine->AddOnScreenDebugMessage() is editor and PIE context only — it does nothing in a shipping build and is meaningless in a headless commandlet. Use UE_LOG(LogYourCategory, ...) as the baseline logging mechanism for any editor tool output that needs to survive outside of a running viewport.

17. When authoring an IDetailCustomization that triggers async operations (asset loads, long validations), use the Slate timer or an editor subsystem to dispatch the work. Do not block the Slate main thread in a button callback — it freezes the entire editor, including the cancel button.

18. FPropertyEditorModule is accessed via FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor"). This module is always loaded in the editor; LoadModuleChecked is appropriate. Do not load it by string in a Runtime module — the module is not present in shipping builds.

19. Editor subsystems (UEditorSubsystem) are the correct place for persistent editor state that should survive selection changes but not survive editor sessions (i.e., not serialized). They initialize with the editor and shut down cleanly. Use them to store shared tool state that multiple editor windows or panels need to read.

20. When a Commandlet needs to modify assets and save them, call UPackage::SavePackage() with the correct flags rather than using the editor's transactional save path. The transactional system is not available in headless context. Set RF_Public and RF_Standalone on newly created assets before saving.

21. Undo/redo integration for custom editor operations requires wrapping modifications in a FScopedTransaction. Without it, Ctrl+Z will not cover your tool's changes, and the editor's dirty-flag tracking will be inconsistent. Use GEditor->BeginTransaction() / GEditor->EndTransaction() or the RAII FScopedTransaction form.

## Smells

- No UnregisterCustomClassLayout() call in ShutdownModule() — crashes on live coding reload or module unload, appearing as an access violation in an unrelated editor system after the tool is not obviously involved
- IDetailCustomization capturing a raw pointer to the customized UObject — the object can be garbage collected while the details panel is open; always use TWeakObjectPtr and check IsValid() before every access
- FSlateApplication::Get() called unconditionally in code shared between commandlet and editor paths — commandlets have no Slate application; this is a null dereference crash that only triggers in CI
- UEditorValidatorBase writing only to UE_LOG without calling AssetFails() — validation failures are invisible to the Content Validation UI and the automated validation pipeline; the tool silently does nothing useful
- Editor Utility Widget used for a CI/automated pipeline task — EUWs require a running editor display and are not invocable from a command line; the correct tool is a Commandlet
- Commandlet used for a designer-facing tool that needs a UI and iterative feedback — commandlets are headless; build an EUW or Blutility utility object instead
- FAssetTypeActions_Base registered but not unregistered in ShutdownModule() — asset browser crashes or incorrect context menus appear for unrelated types after module reload
- LoadObject<T>() or StaticLoadObject() called inside a details customization rebuild — synchronous load on the Slate thread hitches the entire editor; use the Asset Manager async path and refresh the panel in the completion delegate
- Accessing GEditor or GEditorModeTools without checking GEditor != nullptr — both are null in commandlet context and in early engine startup; unconditional access crashes during module startup ordering edge cases
- Editor module declaring a dependency on a Runtime module that in turn has a transitive dependency on the same Editor module — circular dependency causes UBT link error; extract the shared interface to a third module
- FScopedTransaction omitted in a custom editor tool that modifies assets — Ctrl+Z does not undo the changes, leaving the asset in a modified state with no recovery path and confusing the editor's dirty tracking

## Goal
Ensure editor extensions are built with the correct mechanism for their operator and deployment context, registered and unregistered symmetrically to prevent lifecycle crashes, and strictly isolated from runtime code paths so that shipping builds are not contaminated by editor-only APIs. Provide a clear decision framework for choosing between EUW, detail customization, commandlet, and validator patterns based on the tool's requirements.

## Boundaries
- See `build-modules-plugins.md` for Editor module type declaration, StartupModule/ShutdownModule lifecycle, and module dependency rules that enforce Editor/Runtime separation
- See `assets-content-pipeline.md` for FAssetRegistryModule usage (editor-only), commandlet-based cook pipeline integration, and asset saving patterns
