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
* [Minor] If `use.ranks=TRUE`, `Stat` is assigned `modt` directly without zscoreT transformation. It makes sense because zscoreT is anyway only a monotone transformation.
* [Minor] zscoreT uses `approx=TRUE`. This will lead to maybe faster calculation of z-scores of t-distribution and numerically slightly different results, however, the major conclusions should not change much, I hope.
* [Minor] if `iset` is character, it is replaced by the index of IDs. This allows not only integer indices specified as gene-sets, but also gene identifiers 
* [Major] if `fixed.cor` is `TRUE`, `correlation` is set as `inter.gene.cor`, and `vif` is adjusted accordingly (`1+(m-1)*correlation`)
* [Minor] If `fixed.cor` is `TRUE`, the output table has no column `Correlation`

SO the conclusion is that the functionality of biosCamera is highly comparable to camera, with the exception of the handling of inter-gene correlation. Otherwise, the only difference which may lead to a different result is the change in the parameters passed to `zscoreT`, which uses `approx=TRUE` now. Otherwise, the new version of camera improves the robustness of the code, which we shall try to recapitulate in the improved version of biosCamera.

## Thoughts about `inter.gene.cor`

With regard to `inter.gene.cor`, I am not fully comfortable with it, because the assumption that all gene-sets have a intergene correlation of 0.01 is too artificial I think. And even such priors can be useful, I think they should be based on data instead of being based on an arbitrarily chosen number. Alas, in the current implementation of camera.default, the `inter.gene.cor` is assigned uniformly to all gene-sets; a simple change though, can allow a gene-set-specific inter.gene.cor.

In the latest version of ribiosGSEA::biosCamera, I implemented an advanced parameter `.fixed.inter.gene.cor` to allow gene-set specific correlations. [Here's the diff](https://github.com/Accio/ribios/commit/2f9b8b041309ed2d57c6af1c134f00c2d48b9d93#diff-36a02688c4526c5380f8108b487e45ea)

## QR contrast and design

I use an example to illustrate the point - the codes of QR were copied from the camera method.

```{r qr}
library(limma)
group <- gl(3,2)
levels(group) <- sprintf("group%d", 1:nlevels(group))
origDesign <- design <- model.matrix(~group)
colnames(design) <- levels(group)
contrasts <- makeContrasts(contrasts=levels(group)[-1], levels=design)

contrast <- c(0, 0, 1)

(QR <- qr(contrast))
design <- t(qr.qty(QR, t(design)))
if (sign(QR$qr[1, 1] < 0)) 
   design[, 1] <- -design[, 1]
design <- design[, c(2:p, 1)]

y <- matrix(3:8, nrow=1)
QR <- qr(design)
if (QR$rank < p) 
  stop("design matrix is not of full rank")
effects <- qr.qty(QR, t(y))
unscaledt <- effects[p, ]
if (QR$qr[p, p] < 0) 
   unscaledt <- -unscaledt
```

The QR decomposition is used in linear regression to allow efficient calculation of coefficients. Details are given at StackExchange posts like [this one by Matthew Durey](https://stats.stackexchange.com/questions/154485/least-squares-regression-step-by-step-linear-algebra-computation/154514#154514). 

## The high-level, step-by-step summary of camera

In case we do not consider weight of either samples or genes, and do not use ranks.

1. Pre-process and check data
2. Set comparison of interest to the last column of design by simply reordering the columns of the design matrix (contrast is a number), or first QR decomposition (`qr.qty(qr(contrast), t(design))`) which is followed then by reordering.
3. Infer effects (`unscaledt`) of comparison of interest by QR decomposition (`qr.qty(QR, t(y))`)
4. Use residuals of linear fitting to estimate variance per gene, squeeze them (empirical Bayes), and calculate moderated-t statistic
5. Transform the t-statistic to z-scores.
6. For each gene-set
    1. Estimate inter-gene correlation using residuals
    2. Use two-sample t-test to compare difference of the mean z-score of genes within the gene-set, and mean z-score of all genes in the input matrix. Inter-gene correlation is used to adjust the variance
7. Multiple-test correction if needed
8. Report the results
