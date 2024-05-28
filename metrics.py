import pandas as pd

df = pd.read_csv("./results/eval_results4.csv", index_col=0)

# Group by 'env' first, then by 'agent'
grouped = df.groupby(['env', 'agent'])

# Compute mean and standard deviation for each group
result = grouped.agg({'mean_reward': 'mean', 'std_reward': 'std'}).reset_index()
print(result)

envs = df['env'].unique()
for env in envs:
    df_env = df[(df['env'] == env)]
    seeds = df_env['seed'].unique()
    print(f"{env}:{seeds}")
