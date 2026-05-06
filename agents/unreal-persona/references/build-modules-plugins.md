---
name: build-modules-plugins
version: "1.0"
---

# Build System, Modules, and Plugins

## Use This Reference When
- Diagnosing UBT/UHT compilation failures, missing symbol errors, or include path issues
- Designing module boundaries and deciding what belongs in Public vs Private
- Authoring or modifying a .uplugin descriptor or module loading phase
- Debugging packaging or cooking failures that trace back to module type mismatches

## Veteran Expert Stance
Module boundaries are the load-bearing walls of an Unreal project. Engineers who treat .Build.cs as a formality — dumping everything into PublicDependencyModuleNames, using engine-wide umbrella includes, and ignoring module types — pay the debt at cook time, when a shipping build silently drops editor APIs or fails to link. The Public/Private split is not organizational vanity; it directly governs which translation units pay the include cost and which downstream modules inherit compile-time dependencies. Sloppy boundaries mean your 10-module project compiles as if it were one.

UHT and UBT are two separate tools with separate concerns that run in sequence before the C++ compiler touches anything. UHT reads reflection macros and emits .generated.h files; UBT orchestrates module dependency resolution, PCH generation, and compiler invocation. Conflating them — or trying to put complex template expressions inside UCLASS/UPROPERTY macros — is a common source of cryptic parse errors. UHT's parser is not clang; it is a specialized text scanner that breaks on constructs the C++ standard permits.

Plugins are not just module containers; they are isolation units with their own dependency graphs and loading lifecycles. Getting LoadingPhase wrong is a silent runtime bug, not a compile error. A plugin that needs its subsystem initialized before GameInstance must be at PostConfigInit, and shipping that at Default means random init-order failures under specific platform boot sequences that only appear late in QA.

## Core Concerns
- Module type determines which build configurations include the module — Runtime, Editor, Developer, ThirdParty each have distinct inclusion rules
- .Build.cs Public vs Private governs both include path propagation and link visibility to dependent modules
- UHT runs before the compiler; it requires that generated headers are last, and it cannot parse complex C++ template expressions inside reflection macros
- Plugin LoadingPhase controls when module DLLs are loaded relative to engine and game initialization milestones
- Hot reload operates by DLL swap; it does not reconstruct CDOs cleanly and statically-allocated state becomes stale
- Cooking traces hard-reference dependency chains at package level — module type mismatches cause assets or code to be silently dropped from cooked builds

## Practical Heuristics

1. Never put a module that uses Editor APIs (FAssetRegistryModule, IDetailCustomization, UFactory, etc.) as Type = Runtime. It will compile in the editor but fail to link or crash on a cooked build. The correct fix is a separate *Editor module with Type = Editor.

2. PublicDependencyModuleNames is a promise to downstream modules: "my dependents can use types from these modules without declaring them again." Minimize this list. Put headers you expose in your Public/ folder; put everything else in Private/.

3. Follow IWYU strictly. Including CoreMinimal.h is fine for core types, but avoid including Engine.h, UnrealEd.h, or other umbrella headers — they force recompilation of the entire TU on any transitive change and inflate PCH size catastrophically.

4. PrivateIncludePaths entries only affect this module's compilation. They do not propagate. PublicIncludePaths entries are exported to all modules that declare a dependency on this module.

5. The .generated.h file for any header containing reflected types must be the last #include in that header, no exceptions. UHT emits GENERATED_BODY() and GENERATED_UCLASS_BODY() implementations into that file; putting other includes after it produces ODR violations and UHT parse failures.

6. Keep UCLASS/USTRUCT macro arguments simple. UHT's parser does not understand arbitrary C++ — no nested templates, no constexpr expressions, no macro expansions inside the parentheses of reflection macros.

7. When you must reference an Editor-only type inside a Runtime module (rare, usually a mistake), use #if WITH_EDITOR guards and ensure the include itself is also guarded. Failing to guard the include causes a missing symbol at link time in non-editor builds.

8. Circular dependencies between modules are a build error in UBT. Resolve them by extracting shared interfaces or data types into a third, lower-level module that both depend on. Do not use GetModuleChecked<>() as a workaround for a circular compile-time dependency.

9. LoadingPhase = PostConfigInit is the earliest you can reliably use a plugin subsystem before GameInstance::Init(). Default is fine for most gameplay modules. PreLoadingScreen is for things that must exist before the loading screen renders. Getting this wrong produces initialization-order crashes that are timing-dependent and hard to repro.

10. When a plugin declares a dependency on another plugin in .uplugin, UBT enforces load order but does not validate type compatibility. If you depend on a plugin with Editor-only modules, your Runtime module must not statically link against those Editor modules.

11. Hot reload is for iteration speed only. After a hot reload, CDO fields may not reflect newly added UPROPERTY defaults, FName tables can have stale entries, and subsystem OnInitialize callbacks do not re-run. For any state that matters, restart the editor.

12. PrivatePCHHeaderFile in .Build.cs controls which header UBT uses as the PCH for this module. If you have a large stable set of frequently-included headers (Containers, Core, your module's own base types), centralize them in a PCH header and declare it here. Do not fight the automatic PCH selection with bUsePrecompiled = false without a concrete reason.

13. ThirdParty module type is for external pre-built libraries. Set bAddPublicIncludePaths/PublicSystemIncludePaths/PublicSystemLibraryPaths correctly. Never declare a ThirdParty module as Runtime — it bypasses Unreal's symbol visibility management and causes ODR violations on some platforms.

14. Soft plugin dependencies in .uplugin (using the Plugins array with bOptional = true) are loaded if present but do not cause packaging failure when absent. Use this for optional integrations (analytics, platform SDKs) that should not break a stripped build.

15. When diagnosing "cannot open include file" errors in UBT, check three things in order: (a) the module containing the header is listed in dependencies, (b) the include path is in PublicIncludePaths or PrivateIncludePaths of that module, (c) the include statement in your .cpp actually uses the correct relative path form ("Module/ClassName.h" not just "ClassName.h" unless the path root is registered).

16. Developer module type runs in editor and standalone command-line tool builds (Commandlets, ShaderCompileWorker) but is excluded from game client shipping builds. Use it for tooling and automation code that should not ship but is not purely editor UI.

17. Versioning in .uplugin: VersionName is human-readable; Version (int) is machine-compared. Increment Version when module ABI changes to force plugin recompilation in projects consuming binary plugin distributions.

18. EnabledByDefault = false in .uplugin means the plugin is present in the engine or project plugin directory but is not activated unless the .uproject explicitly enables it. This is the correct model for optional platform-specific integrations.

19. bUseUnity = false in .Build.cs disables unity (jumbo) builds for this module. Only do this when you are actively debugging include ordering issues or have headers with conflicting macro definitions. Unity builds are a compile-speed multiplier; disabling them should be temporary.

20. When cooking fails with "unable to find package," first check whether the asset is referenced only through code with a hard UPROPERTY pointer to a type in an Editor module. Cook does not trace through editor types; move the reference to a soft path or a data asset loaded by the Asset Manager.

## Smells

- Every module dependency goes into PublicDependencyModuleNames — exposes all include paths globally, inflates compile time for all dependents, and turns private implementation details into a public contract
- Including Engine.h or UnrealEd.h anywhere outside of legacy migration work — umbrella headers that recompile everything when anything in the engine changes
- Runtime module with direct #include of FAssetRegistryModule or IDetailCustomization without WITH_EDITOR guard — ships as a broken link on consoles and mobile
- .generated.h included anywhere except the last line of its host header — produces hard-to-read ODR or UHT errors that blame the wrong file
- Complex template expressions inside UCLASS() or UPROPERTY() metadata — UHT's parser chokes silently or emits confusing diagnostics
- Plugin with LoadingPhase = Default that its dependents expect to be ready at PostConfigInit — timing-dependent init crash that does not reproduce reliably under debugger attach
- Using GetModuleChecked<T>() at static init time to resolve a circular compile dependency — module may not be loaded yet, causing a check() failure before any game code runs
- Declaring ThirdParty pre-built lib symbols as part of a Runtime module's public API — ODR violations and undefined behavior on platforms with strict symbol visibility
- Hot-reload relied upon to test subsystem init or CDO default changes — CDOs do not reconstruct on hot reload; tests are invalid until editor restart
- bUseUnity = false left permanently in production .Build.cs files — measurable compile-time regression with no benefit after the temporary debugging need is resolved
- Soft plugin dependency (bOptional = true) that the game actually hard-crashes without — optional flags communicate to the packager; they do not provide runtime fallback logic
- Missing ShutdownModule() unregistration of detail customizations or asset type actions — module reload crashes because the stale vtable pointer is called after the DLL is unmapped

## Goal
Ensure module boundaries, dependency declarations, and plugin configurations are structurally correct so that editor builds, cooked shipping builds, and command-line tooling all resolve cleanly without silent omissions or link-time surprises. Prevent the class of bugs where code works in the editor but fails to package, or plugins initialize in the wrong order and produce timing-dependent crashes.

## Boundaries
- See `memory-lifetime-ownership.md` for CDO behavior and object lifetime concerns that interact with hot reload
- See `assets-content-pipeline.md` for how module type affects cook-time asset reference tracing and Asset Manager configuration
- See `editor-tooling.md` for Editor module registration patterns (StartupModule/ShutdownModule, customization registration)
