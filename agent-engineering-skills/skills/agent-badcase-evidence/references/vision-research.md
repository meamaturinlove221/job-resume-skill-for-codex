# Vision research: task-specific evidence

Use these distinctions only for the relevant task.

**Few-shot visual classification:** Baseline/support composition is part of the protocol. If one NG mode is absent from registration, evaluate that specific absent-mode recall and OK recall separately. For paired predictions count rescued and broken items, not just total accuracy. Synthetic success is not real-domain generalization.

**Texture classification:** Check that the label-defining texture changes while background, geometry and render style vary independently. Detect shortcuts on unseen objects/backgrounds and compare other categories before replacing a working baseline.

**3D reconstruction:** Compare predicted geometry in aligned coordinates and matched viewpoints, not only projection overlays or attractive renders. Preserve valid camera estimates when a proposed replacement lacks comparable real evidence; keep geometry and visual gates distinct.

**Thermal rendering:** Compare with the established rendering baseline on the same scene, GT, split and image scale. Read PSNR/SSIM/LPIPS together with whether scene structures remain visible. Verify added physical priors independently before promoting them.

No task-specific datasets, metrics or approval states are provided by this reference: read the actual project records.
