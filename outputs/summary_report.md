# Healthcare Data Analysis Report

## 1. Data cleaning summary

- Raw records: 308
- Duplicates removed: 8
- Invalid values set to missing: 4
- Missing values imputed: 46
- Clean records: 300

## 2. Key findings

- 300 patients analysed; mean age 47.4 years.
- Diabetes prevalence: 21.0%; hypertension prevalence: 26.0%.
- Diabetes prevalence is highest in the 45-59 age group (25.2%).
- BMI and systolic BP are positively correlated (r = 0.32).
- Mean systolic BP: smokers 136.1 vs non-smokers 131.3 mmHg.

## 3. Summary statistics

```
                    count    mean  median    std    min    max      q1      q3
age                 300.0   47.36    46.0  14.49   18.0   90.0   37.75   55.25
bmi                 300.0   25.39    25.2   4.28   15.0   36.5   22.80   28.12
systolic_bp         300.0  132.60   133.0  12.71  101.0  165.0  123.75  140.00
diastolic_bp        300.0   84.03    85.0   8.02   63.0  104.0   79.00   89.25
glucose             300.0  107.53   108.5  19.41   48.2  158.0   94.48  120.02
cholesterol         300.0  217.30   216.1  27.31  149.0  293.4  198.28  235.60
hospital_stay_days  300.0    3.08     3.0   2.14    0.0   12.0    1.00    4.00
```

## Frequency: gender

```
        count  percent
gender                
Female    157     52.3
Male      143     47.7
```

## Frequency: smoker

```
        count  percent
smoker                
No        218     72.7
Yes        82     27.3
```

## Frequency: physical_activity

```
                   count  percent
physical_activity                
Low                  122     40.7
Moderate             113     37.7
High                  65     21.7
```

## Frequency: region

```
         count  percent
region                 
South       82     27.3
West        66     22.0
North       59     19.7
East        57     19.0
Central     36     12.0
```
