I used following commands to compare current biosCamera and the latest camera.default (edgeR:3.20.9)

```{bash colordiff}
colordiff -y --suppress-common-lines -d -b bios-camera.R limma-camera.R
```

I observed following changes (sorted by the order in the code)

* [Minor] Feature count in the gene expression matrix is checked: the function stops if the expression matrix contains fewer than 3 genes
* [Minor] Gene-set length is checked: the function stops if the gene-set list is of length zero
* [Minor] Design matrix is checked for presence, its storage mode (numeric), dimensionality, and df.residual
* [Major] if `inter.gene.cor` is `NA` or `NULL`, `df.camera` is set as `Inf` (which is otherwise `G-2`) in case of using ranks
* [Minor] `unscaledt` is set as `rep.int(0, G)` instead of `rep(0,n)`. The usage of `n` instead of `G` was probably a mistake in the `biosCamera`, which however does not affect the results because the vector is automatically extended.
* [Minor] `ID` is used as name of `unscaledt`.
* [Minor] If `use.ranks=TRUE`, `Stat` is assigned `modt`
* [Major?] zscoreT uses `approx=TRUE`
* [Minor] if `iset` is character, it is replaced by the index of IDs
* [Major] if `fixed.cor` is `TRUE`, `correlation` is set as `inter.gene.cor`, and `vif` is adjusted accordingly (`1+(m-1)*correlation`)
* [Minor] If `fixed.cor` is `TRUE`, the output table has no column `Correlation`

SO the conclusion is that the functionality of biosCamera is highly comparable to camera, with the exception of the handling of inter-gene correlation. Otherwise, the only difference which may lead to a different result is the change in the parameters passed to `zscoreT`, which uses `approx=TRUE` now. Otherwise, the new version of camera improves the robustness of the code, which we shall try to recapitulate in the improved version of biosCamera.

## Thoughts about `inter.gene.cor`

With regard to `inter.gene.cor`, I am not fully comfortable with it, because the assumption that all gene-sets have a intergene correlation of 0.01 is too artificial I think. And even such priors can be useful, I think they should be based on data instead of being based on an arbitrarily chosen number. Alas, in the current implementation of camera.default, the `inter.gene.cor` is assigned uniformly to all gene-sets; a simple change though, can allow a gene-set-specific inter.gene.cor
