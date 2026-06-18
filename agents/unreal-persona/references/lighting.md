---
name: lighting
metadata:
  version: "1.1"
---

# Lighting — Lumen GI, Light Mobility, and Post Process

## Use This Reference When
- Configuring or debugging Lumen global illumination, reflections, or emissive light propagation
- Choosing light mobility (Static, Stationary, Movable) and understanding the bake and runtime implications of each
- Diagnosing visual artifacts: GI leaking through geometry, splotchy indirect shadows, over-exposed characters in different lighting zones, or missing reflections on translucency
- Tuning Post Process Volume settings for exposure, bloom, tone mapping, or Lumen quality overrides per zone

## Veteran Expert Stance
Lumen is not a magic "dynamic GI on" toggle. It is a system of interconnected subsystems — mesh distance fields, surface cache, screen-space probes, and hardware ray tracing as an optional acceleration layer — and each link in that chain has failure modes that produce silent, incorrect results rather than errors. The most expensive mistakes happen when teams treat `r.Lumen.*` cvars as the primary quality control surface and ignore the upstream requirements: distance fields must be generated, mesh sizes must be sufficient for distance field resolution, and emissive materials must cross the minimum brightness threshold before Lumen registers them as light sources. Diagnosing Lumen problems means working from first principles, not from cvar tweaking.

Light mobility is a choice made at level design time with long-lasting consequences. Switching a directional light from Movable to Stationary mid-production requires a lighting rebuild, and a mismatched mobility setup — where a `Static` sky light coexists with `Movable` fill lights — produces visually incorrect results that are hard to attribute to a single cause. The rule is to decide mobility before scene population and to document the lighting contract for each scene type in the project. Lumen scenes are `Movable` throughout; fully baked scenes use `Static` or `Stationary` strategically. Mixing is a red flag.

Post Process Volumes are a first-class gameplay tool, not just artist polish. Auto-exposure is the main reason characters look wrong when transitioning between interior and exterior spaces, and it is controlled per-volume with per-volume blend radii. Understanding the EV100 range, the adapt speed, and the distinction between metering modes is prerequisite knowledge for shipping a game with consistent visual readability across all environments. A PostProcessVolume with `BlendRadius=0` and highest `Priority` is effectively a global override — use that pattern deliberately when you need guaranteed values in specific areas (cinematic zones, tutorial sequences, boss arenas).

## Core Concerns
- Lumen's dependency chain: project-level distance field generation → per-mesh distance field quality → surface cache resolution → probe density → final GI quality. Failures at any link cascade to the output.
- Light mobility contract: `Static` (fully baked), `Stationary` (baked shadow maps + dynamic lighting), `Movable` (fully dynamic). Each has a distinct performance and quality profile and is not freely interchangeable at runtime.
- Sky Light role: the ambient fill source for the entire scene. Its mobility and recapture settings determine whether indirect lighting updates at all. A misconfigured Sky Light undermines all other GI work.
- Post Process Volume priority and blend radius: global volumes vs. local zone overrides, exposure management, and Lumen quality overrides per zone.
- Nanite integration: Nanite meshes are the ideal Lumen input. Non-Nanite meshes require explicit distance field generation settings, and foliage has additional per-instance GI constraints.
- Reflection pipeline: Lumen Reflections replace capture-based reflections for opaque surfaces; translucency still falls back to Sphere/Box Reflection Captures or Screen Space Reflections.

## Practical Heuristics

1. Enable `Generate Mesh Distance Fields` globally in Project Settings > Rendering before enabling Lumen. Individual meshes can override this, but the global setting is the baseline. Without distance fields, Lumen falls back to screen-space-only GI, which is materially worse for any off-screen occluded surfaces.

2. Lumen software mode traces against mesh distance fields and screen-space scene data. It is not hardware ray tracing. Hardware RT (`r.Lumen.HardwareRayTracing 1`) is an optional acceleration path that improves accuracy and removes some distance field artifacts but requires compatible GPU and platform support. Design around software Lumen and treat hardware RT as a quality tier upgrade.

3. Directional light mobility for a Lumen scene: use `Movable`. `Stationary` with Lumen works but produces shadow map artifacts where the two systems disagree. `Static` directional light with Lumen enabled produces no dynamic GI update whatsoever — the most common cause of "Lumen is doing nothing" reports.

4. Sky Light `bRealTimeCapture=true` regenerates the sky cube map every frame. This is expensive and typically reserved for skies with dynamic cloud simulation. For most scenes, recapture on demand or use a static capture with a period update. Always verify the Sky Light is set to `Movable` in Lumen scenes, or indirect lighting will not respond to time-of-day changes.

5. Emissive materials must exceed the project-level `Emissive Boost` threshold to register as Lumen light sources. If an emissive surface is not contributing to GI, check `r.LumenScene.EmissiveBoost` and the material's emissive output value. Extremely high emissive values also cause over-bright surface cache entries — cap via the project Emissive Clamp settings rather than in the material.

6. Lumen does not handle translucency well. Transparent surfaces (glass, water, volumetric fog) do not contribute to Lumen GI and do not receive it accurately. Use Reflection Captures, Screen Space Reflections, or planar reflections for transparent surface reflections. This is a hard technical boundary, not a tuning issue.

7. `PostProcessVolume` with `BlendRadius=0` and `bUnbound=true` is a global volume. Set `Priority` deliberately — higher priority wins when volumes overlap. For per-zone quality overrides (performance-sensitive combat arenas vs. high-quality cinematics), use bounded volumes with a short blend radius at the transition boundary.

8. Auto-exposure (`EV100` range, `MinBrightness`, `MaxBrightness`, `SpeedUp`, `SpeedDown`) should be set explicitly in every shipping project rather than relying on engine defaults. The default range is wide enough to cause jarring transitions. Narrow the range per zone and use the histogram metering mode for more stable results in scenes with extreme contrast (torches in a cave, monitors in a dark room).

9. `Stationary` lights have a hard limit of four overlapping Stationary lights per surface before the engine falls back to fully dynamic rendering for excess lights. This limit is a common source of unexpected dynamic shadow cost in dense interior scenes. Use the Light Complexity view mode to detect violations.

10. Lumen GI leaks through thin geometry because distance fields are approximate representations of mesh volume. Thin walls (less than ~15cm on default distance field resolution) may not fully block distance field rays. The fix is to increase wall thickness in the mesh, increase the mesh's distance field resolution override, or add Shadow Bias compensation on the light. Do not paper over the symptom by boosting `r.Lumen.Scene.SurfaceCacheResolution` — address the geometry.

11. Sphere and Box Reflection Captures are still necessary in Lumen scenes for translucent surfaces. Place them in areas with translucent materials (windows, water bodies) and keep their radius tight. They no longer drive opaque surface reflections in Lumen mode, so count them only where translucency exists.

12. Nanite meshes contribute to Lumen surface cache without requiring distance field geometry. Non-Nanite meshes require `Enable Distance Field Geometry` checked on the static mesh asset. For foliage using Nanite, verify `Lumen` is enabled in the Foliage Type settings, or per-instance GI will be absent.

13. Lumen's `FNiagaraSystemScalabilitySettings` equivalent for lighting is the Scalability Group system under `r.Lumen.*` scalability settings. Expose Lumen quality reduction through the engine scalability groups (Low/Medium/High/Epic) rather than hardcoding `r.Lumen.DiffuseIndirect.Allow 0` in a config file. This integrates properly with device profiles on console.

14. Indoor scenes with small exterior light openings (windows, skylights) are the hardest case for Lumen. The surface cache probe density at a typical door frame may not capture enough indirect bounce data to light deep interior surfaces. Compensate with a low-intensity Sky Light contribution baked as a subtle fill, a secondary small Rect Light at the opening, or increase `r.LumenScene.SurfaceCacheResolution` specifically for that scene (via Post Process Volume Lumen override).

15. Bloom and lens flare are independent settings in Post Process Volume. Bloom `Intensity` and `Threshold` are the primary performance knobs. Disabling bloom entirely is a common mobile optimization but has a disproportionate visual impact — prefer reducing `Intensity` and raising `Threshold` before disabling.

16. When using a time-of-day system (rotating directional light, dynamic sky), the Sky Light must recapture on each update cycle. Calling `USkyLightComponent::RecaptureSky()` explicitly from C++ at the update interval is more controlled than `bRealTimeCapture=true` and cheaper when time-of-day advances in discrete steps.

17. Lumen reflections replace `r.SSR` (Screen Space Reflections) for opaque surfaces automatically when Lumen is enabled. If SSR artifacts are visible alongside Lumen reflections, check that `r.SSR.Quality` is set to 0 or that the SSR pass is explicitly disabled in the Post Process Volume — Lumen and SSR can coexist and double-cost if both are active.

18. Splotchy indirect shadows in Lumen output are typically caused by insufficient probe density or large surfaces with low surface cache texel density. Before increasing resolution settings, first check whether the affected mesh has a very large UV island scale or an exceptionally large world-space footprint — breaking a large ground plane into smaller tiles often resolves splotch artifacts more efficiently than raising resolution.

## Smells

- `Static` mobility on a Directional Light or Sky Light while Lumen GI is enabled — the GI will not update and scene looks perpetually flat or incorrect.
- Four or more overlapping `Stationary` lights on the same surface, triggering silent fallback to dynamic rendering.
- Emissive materials intended as GI contributors with output values below the Lumen emissive boost threshold, generating no visible indirect contribution.
- `bRealTimeCapture=true` on Sky Light in a scene without a dynamic sky — paying per-frame capture cost for a static result.
- Thin walls (under ~15cm effective distance field volume) in an indoor Lumen scene without distance field resolution overrides, causing persistent GI leak.
- No `PostProcessVolume` hierarchy defined — every zone using the same global exposure and tone mapping settings, making lighting zones visually indistinct.
- `r.Lumen.*` cvars hardcoded in `Engine.ini` or `DefaultEngine.ini` instead of exposed through scalability groups, bypassing device profile management on console.
- Non-Nanite foliage meshes without `Enable Distance Field Geometry` checked, silently contributing no Lumen surface cache data.
- Bloom and SSR both active alongside Lumen Reflections on opaque surfaces, doubling reflection cost with no visual benefit.
- Auto-exposure with default EV100 range in a scene mixing outdoor daylight and underground caves, causing severe exposure whiplash on level transition.
- Sphere Reflection Captures placed to cover large open areas in a Lumen scene where they have no effect on opaque reflections, wasting capture overhead.
- Treating the Lumen quality issue as purely a cvar tuning problem before verifying that mesh distance fields are generated and correctly resolved.

## Goal

This reference provides the factual basis for correct Lumen configuration, light mobility selection, and Post Process Volume management in a shipping Unreal Engine 5 project. It targets the specific failure modes that cost the most time in production — wrong mobility contracts, silent GI failures from missing distance fields, and exposure inconsistency between lighting zones.

## Boundaries

- See `materials.md` for emissive material setup, emissive boost interaction with Lumen, and translucency shading model constraints.
- See `performance-profiling.md` for interpreting GPU profiler output specific to Lumen cost (LumenScene, LumenReflections, LumenDiffuseIndirect passes) and correlating to frame budget.
- See `niagara-fx.md` for Niagara Light Renderer module behavior and its interaction with dynamic lighting budgets.
