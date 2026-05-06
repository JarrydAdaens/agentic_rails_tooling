---
name: assets-content-pipeline
version: "1.0"
---

# Assets and Content Pipeline

## Use This Reference When
- Diagnosing unexpected cooked build size, missing assets at runtime, or cook-time reference trace failures
- Designing data loading strategies for open-world streaming, DLC, or chunked delivery
- Choosing between hard references, soft references, and Asset Manager patterns for a new system
- Debugging FStreamableHandle lifetime issues, premature asset unloads, or hitches caused by synchronous loads on the game thread

## Veteran Expert Stance
Hard references are a tax. Every UPROPERTY pointer to a UObject subtype forces that object — and its entire transitive hard-reference graph — to be loaded into memory when the referencing asset loads, and to be included in any cook chunk that contains the referencing asset. Engineers who use TArray<UTexture2D*> in a GameInstance-level config asset have often unknowingly pulled their entire texture atlas into memory at boot. The discipline is to make the default soft and promote to hard only when you have a proven need for synchronous access.

The Asset Manager and FStreamableManager are the correct runtime loading API, not LoadObject<T>() or StaticLoadObject(). Synchronous load on the game thread stalls rendering and audio for however long the IO takes. In a cooked shipping build on a slow storage device, "however long" can be hundreds of milliseconds. The async-load-with-callback pattern is not optional polish; it is the correct default. The only legitimate use of LoadSynchronous() is in editor utilities, commandlets, and module startup code that runs before the game loop.

Content pipeline discipline — consistent folder structure, redirector fixup, Primary Asset labeling, and chunk assignment — is infrastructure work that pays off at every ship milestone. Teams that skip it discover at alpha that their 40 GB build is unsplittable, their DLC patches include assets from the base game, and their streaming level cook times are dominated by chasing redirectors. Retrofitting this structure under time pressure is painful. It belongs in the project foundation.

## Core Concerns
- Hard vs soft reference determines both runtime memory load behavior and cook-time dependency graph inclusion — the two effects are linked
- FStreamableHandle lifetime directly controls whether a loaded asset stays resident or is immediately eligible for GC
- Primary Asset IDs and chunk assignment govern how the cooker partitions content for streaming installs and DLC
- Asset Manager async loading is the correct default for all gameplay-path content loading; synchronous load is the exception
- Redirectors left unfixed accumulate into load-time overhead and cook graph complexity that compounds over the project lifetime
- FAssetRegistryModule is editor-only; all runtime content queries must go through Asset Manager or TSoftObjectPtr patterns

## Practical Heuristics

1. Default to TSoftObjectPtr<T> for any asset reference stored in data (DataAssets, config UObjects, savegame-adjacent structs). Upgrade to a hard UPROPERTY pointer only when profiling confirms the asset must always be resident and the load cost is acceptable at the referencing asset's load point.

2. TSoftClassPtr<T> instead of TSubclassOf<T> in data assets that reference Blueprint subclasses. TSubclassOf<UBaseAbility> in a PrimaryDataAsset will hard-reference every Blueprint ability subclass through the class default object chain, loading all of their textures, meshes, and audio at data asset load time.

3. FStreamableHandle must be kept alive for as long as the asset needs to stay loaded. Assign it to a UPROPERTY TSharedPtr<FStreamableHandle> member, or store it in a manager. A handle that goes out of scope releases the streaming pin, and GC will collect the asset on the next pass — typically within seconds, causing intermittent "asset unloaded mid-use" crashes that are nearly impossible to reproduce deterministically.

4. RequestAsyncLoad returns immediately and calls the delegate on the game thread when loading completes. Do not access the loaded asset from inside the lambda without verifying the handle is still valid and the owning UObject has not been destroyed (use TWeakObjectPtr for the outer or check IsValid()).

5. LoadSynchronous() is acceptable in: editor tools, commandlets, module StartupModule(), and any code path that runs before BeginPlay(). It is not acceptable in BeginPlay(), Tick(), or any event-driven gameplay path. If you find yourself calling it in gameplay code, the architecture needs to change.

6. Primary Asset IDs (FPrimaryAssetId) are the unit of Asset Manager control. Assign a type tag and name to every UPrimaryDataAsset subclass that should be individually loadable, cookable, or chunk-assignable. Without a Primary Asset ID, the Asset Manager cannot enumerate, bundle, or async-load the asset by label.

7. Chunk assignment via Primary Asset Labels lets you express "these 200 gameplay assets belong to level zone 3" without modifying every asset individually. One UPrimaryDataAsset with AssetBundleData pointing at the zone's content is cleaner and more maintainable than per-asset chunk metadata.

8. Run Fixup Redirectors (Editor → Asset Actions → Fix Up Redirectors in Folder) before every milestone branch cut. Unfixed redirectors add an indirection step on every asset load along that path, and the cook traces through them, doubling the reference-tracing work for assets at the end of a long redirector chain.

9. Moving or renaming an asset without fixing the redirector immediately afterward is always wrong in a shared repository. Other engineers' maps, Blueprints, and data assets will silently hold a redirector reference that works in the editor but adds overhead and eventually breaks if the original asset location is cleaned up.

10. Assets referenced only by C++ code (not by any content package) will not be cooked unless explicitly added to the cook list or the Asset Manager's primary asset scan paths. Use soft references with explicit async loads, register the asset as a Primary Asset, or add it to AdditionalCookPackages in the project settings. An asset that exists on disk but is unreachable from the content dependency graph is silently missing from the cooked build.

11. FAssetRegistryModule::Get().GetAssets() and related queries are editor-only. Any code that calls into AssetRegistry at runtime must be inside #if WITH_EDITOR or the module type must be Editor. For runtime enumeration of assets by tag or type, use UAssetManager::Get().GetPrimaryAssetIdList() and related Asset Manager queries.

12. DataTable row types (USTRUCT with GENERATED_BODY()) add zero memory at DataTable load time for rows not accessed — the DataTable loads all rows together. For very large tables, consider splitting by gameplay domain or using asset-per-row UDataAsset patterns with lazy loading per entry.

13. Asset Bundle entries in FAssetBundleData (declared in UPrimaryDataAsset::AssetBundles) are named groups of soft references that the Asset Manager can load or unload as a unit. Use them to model "active loadout" vs "preview thumbnail" levels of content for the same primary asset.

14. UPrimaryDataAsset subclasses should not themselves hold hard UPROPERTY references to other large assets unless those assets must always co-load. The whole point of primary asset modeling is that load scope is explicit and controllable; a hard reference defeats that.

15. Soft references survive cooking as path strings; they do not require the target to be reachable from any hard-reference chain. But the target still must be either a primary asset or referenced somewhere by a primary asset's bundle, or it will not be in the cooked build at all.

16. FSoftObjectPath can be constructed and resolved at runtime from a string. This is how you can load assets whose paths are determined by data (e.g., a table-driven skin system). Validate the path before calling RequestAsyncLoad — an invalid FSoftObjectPath will silently call the completion delegate with a null object rather than asserting.

17. Streaming level content and sublevel packages must be cookable from the persistent level's dependency graph. If a sublevel contains a hard reference to a type only reachable from the editor (e.g., a FEditorOnlyDataType field on an actor in the sublevel), that sublevel will fail to cook cleanly. Use WITH_EDITORONLY_DATA guards on editor-only fields in actor and component types.

18. Content folder structure should reflect streaming and delivery boundaries, not just organizational aesthetics. Chunk assignment is based on directory rules in DefaultGame.ini's [/Script/UnrealEd.ProjectPackagingSettings] PrimaryAssetTypesToScan. Consistent naming (Content/Maps/Zone1/, Content/Characters/Enemies/) maps cleanly to chunk rules.

19. Thumbnail rendering in the editor creates hidden hard references from the thumbnail cache to assets. This is normal editor behavior, but it means the asset registry can show false-positive dependency counts in editor. Always verify dependency graphs from a cook trace, not from the editor's reference viewer alone.

20. When using async loading for UI (e.g., loading a character portrait on hover), always cancel or ignore the completion delegate if the requesting widget is destroyed before the load completes. Store the FStreamableHandle in the widget's UPROPERTY and release it in the widget's NativeDestruct or Destruct.

## Smells

- TSubclassOf<UBaseAbility> or UTexture2D* in a UPrimaryDataAsset that is loaded at startup — forces the entire transitive asset graph into memory at boot, often 10–100x the intended memory cost
- FStreamableHandle stored as a local variable or raw function parameter — asset is pinned only for the call duration; GC collects it before the first frame that needs it
- LoadSynchronous() called in BeginPlay() or Tick() — synchronous disk IO on the game thread; will hitch on any platform with real storage latency
- Assets moved via the OS file system or Perforce without using the editor's asset rename/move — creates broken references rather than redirectors, causing silent null at runtime
- Unfixed redirectors accumulated over multiple milestones — load-time overhead, cook graph complexity, and eventual breakage when the source path is cleaned
- No Primary Asset labeling or chunk assignment in a project that will use streaming installs or DLC — impossible to split the cooked build without retrofitting the entire content hierarchy
- FAssetRegistryModule called from a Runtime module without WITH_EDITOR guard — missing symbol at link time in shipping builds
- TSoftObjectPtr resolved via .Get() without first checking if it is already loaded — returns null silently if the async load has not completed; should check .IsValid() or use the streamable handle's completion delegate
- Content assets that are only referenced from C++ code with no primary asset registration — silently absent from cooked builds with no cook error
- DataTable holding thousands of rows with large embedded struct fields (mesh references, large FText arrays) loaded as a single monolithic package — no per-row streaming granularity; entire table loaded or nothing

## Goal
Ensure that content loading scope, cooking inclusion, and streaming granularity are explicitly controlled through soft references, Asset Manager primary asset labeling, and async loading patterns — so that cooked build size, memory usage, and streaming hitches are predictable, measurable, and bounded. Prevent the class of bugs where assets are unexpectedly large in memory, missing in shipping builds, or loaded synchronously on the game thread.

## Boundaries
- See `build-modules-plugins.md` for how module type (Runtime vs Editor) determines which code paths participate in cook-time asset tracing
- See `memory-lifetime-ownership.md` for GC interaction with streamed assets, UObject lifetime, and UPROPERTY-pinned references
- See `editor-tooling.md` for FAssetRegistryModule usage patterns that are valid only in editor modules
