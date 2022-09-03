# Vehicle insurance cross-sell
<p align="center"><img src="reports/imgs/banner.png"></p>
<sub>Author: Gabriel O. Cenciati</sub><br>
<sub>Date: 04-21-2022</sub>

---

# Table of contents
  1. Business problem
  2. Strategy
  3. Insights
  4. Solution
  5. Conclusions
  6. References

---

# 1. Business problem
## 1.1. Introduction
An insurer that provides health insurance to its customers needs help building a model to rank last year's customers in order of propensity to buy new insurance because it does not have enough money to spend convincing each customer separately.

**Problem statement:** Build a model to rank the most likely customers who would be interested in vehicle insurance.

## 1.2. Target metric
Our interest here is to evaluate how good the ranking made by the model was. That said, a great option is to use a metric that takes into account all relevant customers ranked out of K people previously defined, and that is exactly what a metric called Precision at K or Precision@K does.

* Where relevant customers are those who will be really interested to buy a vehicle insurace.
* Where K is the number of feasible people to the company get in touch and offer the product.

<br>

<p name="precision-at-k" align="center"><img src="reports/imgs/precision-at-k.png"></p>

## 1.3. Assumptions
Here is what I assumed to move forward with this project:
* People who do not have a driving license but have a vehicle in their name were all considered valid because the column that identifies having or not may cover people who do not have it active at the moment.

---

# 2. Strategy
## 2.1. CRISP-DM
CRISP-DM stands for cross-industry process for data mining. The CRISP-DM methodology provides a structured approach to planning a data mining project. It is a robust and well-proven methodology.

This model is an idealised sequence of events. In practice many of the tasks can be performed in a different order and it will often be necessary to backtrack to previous tasks and repeat certain actions. The model does not try to capture all possible routes through the data mining process.
<p align="center"><img src="reports/imgs/crisp-methodology.jpg"></p>

## 2.2. Steps
### 2.2.1. Project architecture
<p align="center"><img src="reports/figures/project-architecture.png"></p>

### 2.2.2. Data pipeline
* Business understanding
0. Data acquisition
1. Data cleaning and description
2. Feature engineering
3. Exploratory data analysis
4. Data balancing
5. Data preprocessing
6. Feature selection
7. Machine learning modeling
8. Hyperparameters fine-tuning
9. Calibration
10. Deployment

### 2.2.3. Model lifecycle
Placeholder

---

# 3. Insights
## 3.1. Hypotheses
<img src="reports/imgs/mind-map.png">
<img src="reports/imgs/hypotheses-list.png">

## 3.2. Exploration
<p align="center"><img src="reports/imgs/insight-01.png"></p>

<br>

<p align="center"><img src="reports/imgs/insight-02.png"></p>

<br>

<p align="center"><img src="reports/imgs/insight-03.png"></p>

<br>

<p align="center"><img src="reports/imgs/insight-04.png"></p>

<br>

* In the feature selection step, the two methods used in this project to prioritize the columns (Boruta and Feature importance) said that having damaged the vehicle is one of the most meaningful columns for the final algorithm's decision.
<p align="center"><img src="reports/imgs/insight-05.png"></p>

---

# 4. Solution
## 4.1. Algorithm applied
The best performance was by a Random Forest Classifier, an ensemble type of algorithm which is a set of other less complex algorithms (in this case, decision trees). Despite the fact that it has outperformed every tested algorithm, one of its biggest cons is the computational cost that, depending on the dataset, can become as costly as possible.

## 4.2. Performance and impact
* As reported, it had an excellent performance compared to other algorithms, getting 83.68% of precision@33.000. This means that more than 80% of 33.000 customers out of 70.000 who were considered relevant by the model have a significant chance of becoming clients of the new insurance.

<br>

1. **Cumulative gains curve**: indicates the relationship between the percentage of sample (users in the dataset) and the number of interested people that our model is able to classify in that certain sample percentage. In this case, the trained model was able to include 80% of interested customers using only 40% of the dataset.
2. **Lift curve**: indicates how good is the trained model compared to a random selection of potential customers. In this case, the trained model is more than 2 times better than just a random model.
<p align="center"><img src="reports/imgs/model-performance-01.png"></p>

<br>

* Many machine learning algorithms are probabilistic, meaning they can calculate a probability of belonging to a certain class. Unfortunately, most of them, like the one used in this project, are not well calibrated. This means that they may be over-confident in some cases and under-confident in other cases.
* Therefore, it is often a good idea to calibrate the predicted probabilities for nonlinear machine learning models. However, in this specific case, the calibration had a worse performance in terms of confidence than the not calibrated model.
<p align="center"><img src="reports/imgs/model-calibration-01.png"></p>

<br>

* Both were evaluated through the Brier score loss, and as you can see below the calibrated model was a slightly worse.
<div align="center">
  <img src="reports/imgs/brier-score-loss.png">
  <img src="reports/imgs/model-calibration-02.png">
</div>

---

# 5. Conclusions
## 5.1. Results
* Now the business team can easily predict and rank as many users as they want through an integrated REST API hosted on cloud and being used by scripts in Google sheets just by writing each customer's information and clicking on "propensity score" at the top of the page.
<p align="center"><img src="reports/imgs/results01.gif"></p>

## 5.2. What's next
* Deal in a different way with outliers.
* Create polynomial features.
* Try using target encoder.
* Compare a calibrated LightGBM to a calibrated Catboost.

---

# 6. References
[1] https://www.sv-europe.com/crisp-dm-methodology/

[2] [Wikipedia - Learningto rank](https://en.wikipedia.org/wiki/Learning_to_rank)

[3] [Recall and Precision at K for Recommender Systems](https://medium.com/@m_n_malaeb/recall-and-precision-at-k-for-recommender-systems-618483226c54)

[4] BROWNLEE, Jason. Data Preparation for Machine Learning: Data Cleaning, Feature Selection, and Data Transforms in Python. 1. ed. 2020.

[4] [Machine Learning Mastery - Probability calibration for imbalanced classification](https://machinelearningmastery.com/probability-calibration-for-imbalanced-classification/)

[6] https://www.youtube.com/watch?v=w3OPq0V8fr8

[7] [DataTalksClub](https://www.youtube.com/c/DataTalksClub)

[8] [MLOps Guide](https://mlops-guide.github.io/)
