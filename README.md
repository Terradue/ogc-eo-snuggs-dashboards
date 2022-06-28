## Installation 

Create and activate the conda environment.

Run `streamlit run dashboards/app.py` 


## Expressions examples

### RGB Composites

Pre-event acquisition true-colour RGB composite

```
(riocolor 'Gamma RGB 3.5 Saturation 1.5 Sigmoidal RGB 6 0.55' (asarray (interp red1 (asarray 0 10000) (asarray 0 1)) (interp green1 (asarray 0 10000) (asarray 0 1)) (interp blue1 (asarray 0 10000) (asarray 0 1))))
```

Pre-event acquisition false-colour RGB composite

```
(riocolor 'Gamma RGB 3.5 Saturation 1.5 Sigmoidal RGB 6 0.55' (asarray (interp nir1 (asarray 0 10000) (asarray 0 1)) (interp red1 (asarray 0 10000) (asarray 0 1)) (interp green1 (asarray 0 10000) (asarray 0 1))))
```


Post-event acquisition true-colour RGB composite

```
(riocolor 'Gamma RGB 3.5 Saturation 1.5 Sigmoidal RGB 6 0.55' (asarray (interp red2 (asarray 0 10000) (asarray 0 1)) (interp green2 (asarray 0 10000) (asarray 0 1)) (interp blue2 (asarray 0 10000) (asarray 0 1))))
```

Post-event acquisition false-colour RGB composite

```
(riocolor 'Gamma RGB 3.5 Saturation 1.5 Sigmoidal RGB 6 0.55' (asarray (interp nir2 (asarray 0 10000) (asarray 0 1)) (interp red2 (asarray 0 10000) (asarray 0 1)) (interp green2 (asarray 0 10000) (asarray 0 1))))
```

### Change detection

#### Change Vector Analysis

```
(threshold_otsu (cva (standardization (asarray red1 green1 blue1 nir1)) (standardization (asarray red2 green2 blue2 nir2))))
```

#### k-means classification 


```
(kmeans 5 (asarray red1 green1 blue1 nir1 red2 green2 blue2 nir2 (pca 1 (asarray red1 green1 blue1 nir1 red2 green2 blue2 nir2)) (pca 2 (asarray red1 green1 blue1 nir1 red2 green2 blue2 nir2)) (pca 3 (asarray red1 green1 blue1 nir1 red2 green2 blue2 nir2))))
```
