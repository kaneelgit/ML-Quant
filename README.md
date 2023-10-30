# ML-Quant
Notebooks and Code for ML based quant strategies and research.

## Annotations and Sampling

### Trend prediction using a Gaussian Mixture Model
Original data distribution, prediction by a mixture distribution implemented using tensorflow probability(TFP) and the prediction by sklearn Gaussian Mixture Model.
![gmm_mixture_data](https://github.com/kaneelgit/ML-Quant/assets/85404022/f6b0b76d-8f23-4626-8e0c-71a55a721af8)

TFP mixture model components

![Mixture model components ](https://github.com/kaneelgit/ML-Quant/assets/85404022/8934afc3-7cf7-4e2f-a75e-d166a1e98401)

Predicted trends by the mixture model
![predicted trend from mixture model](https://github.com/kaneelgit/ML-Quant/assets/85404022/926c70e7-8cc2-40f1-a7f1-5d8c06eb37cf)

### Volume bar sampling
Here we sample and plot 'close' value based on the volume. (Close value at every "xx" volume)
![VolumeBarSamples](https://github.com/kaneelgit/ML-Quant/assets/85404022/79adf80e-8f49-4cfa-aed0-c845aab7d052)

### Trend strength and trend period
Here we generate trends (% increase or decrease in SPY) and find the trend strength (value between 0 and 1 depending on how long the trend last) and trend period (how long the trend last).
![TrendStrength](https://github.com/kaneelgit/ML-Quant/assets/85404022/a11d9f7f-ee22-4dfa-86e8-67c8f94ba04f)
![trend_period](https://github.com/kaneelgit/ML-Quant/assets/85404022/a3b697b5-09d4-43aa-ae6d-32b7325dbf26)


## EMA Optimization
This notebook has a method to find the best EMA lines that represent 'uptrends' and 'downtrends' in S&P 500.

![ema optimize](https://github.com/kaneelgit/ML-Quant/assets/85404022/5eda7ba5-bec7-4602-b0c8-bf9742ffaa1b)

![ema optimized](https://github.com/kaneelgit/ML-Quant/assets/85404022/e8579eab-7cb6-478d-b9e5-0b52580ed130)

## Probabilistic Logistic Regression
This shows how to use probabilistic Logistic Regression to detect outliers in a dataset. Prob LR is useful to guage the confidence of a decision. This is helpful to decide the risk of a bet. 

![prob_logr](https://github.com/kaneelgit/ML-Quant/assets/85404022/bd3dddaf-4364-49b6-8ad0-9c9132ddd981)

![model_results](https://github.com/kaneelgit/ML-Quant/assets/85404022/1429866a-553a-42c7-84ed-198e92f2cd23)

## Probabilistic Linear Regression

![priceranget1](https://github.com/kaneelgit/ML-Quant/assets/85404022/b835b6d6-af3f-45a0-81d5-2d9cbdb07d57)

![priceranget2](https://github.com/kaneelgit/ML-Quant/assets/85404022/704b4cb0-8452-4d3a-b2d5-c8ff10549c84)

![prob_lr](https://github.com/kaneelgit/ML-Quant/assets/85404022/c3069aa7-67b4-420c-a595-71eb2b689a9a)

## Unsupervised Buy-Sell detection

![outliers](https://user-images.githubusercontent.com/85404022/219976291-3b833654-fa04-4009-ae5f-f7139881732e.png)


