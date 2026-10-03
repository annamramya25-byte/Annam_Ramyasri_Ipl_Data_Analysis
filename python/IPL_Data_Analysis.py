import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# ============================================================
#  LOAD DATASET
# ============================================================
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
deliveries.columns = (
    deliveries.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
)
print("DELIVERY COLUMNS:", deliveries.columns.tolist())
print("\n================================================")
print("DATASET LOADED SUCCESSFULLY")
print("================================================")
print(matches.head())
# ============================================================
#  BASIC DATASET INFORMATION
# ============================================================
print("\n================================================")
print("FIRST 5 RECORDS")
print("================================================")
#=======================================================
# Display the last five recors
#=======================================================
print(matches.head())
print("\n================================================")
print("LAST 5 RECORDS")
print("================================================")
# ====================================================
#  check the dataset shape
#====================================================
print(matches.tail())
print("\n================================================")
print("DATASET SHAPE")
print("================================================")
# =================================================
# Display the columns names
#====================================================
print("Rows and Columns:", matches.shape)
print("\n================================================")
print("COLUMN NAMES")
print("================================================")

print(matches.columns)


print("\n================================================")
print("DATA TYPES")
print("================================================")
print(matches.dtypes)


print("\n================================================")
print("DATASET INFORMATION")
print("================================================")

matches.info()

# ============================================================
# NUMERICAL AND CATEGORICAL COLUMNS
# ============================================================

print("\n================================================")
print("NUMERICAL COLUMNS  ")
print("================================================")

print(matches.describe())
print("\n================================================")
print("CATEGORICAL COLUMNS")
print("================================================")

print(matches.describe(include="object"))
# ========================================================
# CHECK THE Data types  OF EACH COLUMN
#=========================================================
print("\n===============================================")
print("MATCHES - DATA TYPES")
print("=================================================")
print(matches.dtypes)
# ====================================================
#  BASIC STATISTICAL INFORMATION
#=================================================
print("\n=============================================")
print("MATCHES - BASIC STATISTICS")
print("==============================================")
print(matches.describe(include="all").T)

print("\n=============================================")
print("DELIVERIES - DATA TYPES")
print("================================================") 
print(deliveries.dtypes)

print("\n===============================================")
print("DELIVERIES - BASIC STATISTICS")
print("=============================================")
print(deliveries.describe(include="all").T)
 # =======================================================
 #  MISSING VALUES
 # =======================================================
print("\n==============================================")
print("\nMATCHES - MISSING VALUES")
print("================================================")
print(matches.isna().sum())
print("\n==============================================")
print("\nDELIVERIES - MISSING VALUES")
print("================================================")
print(deliveries.isna().sum())
# =======================================================
# check DULPLICATE VALUES
# =======================================================
print("\n==============================================")
print("DUPLICATE RECORDS")
print("================================================")
print("Duplicate rows in matches:", matches.duplicated().sum())
print("Duplicate rows in deliveries:", deliveries.duplicated().sum())
print("\nDuplicate match records:")
print(matches[matches.duplicated(keep=False)].head(10))

print("\nDuplicate delivery records:")
print(deliveries[deliveries.duplicated(keep=False)].head(10))
# ============================================================
#  Remove dulpicate records
# ===========================================================
matches = matches.drop_duplicates().copy()
deliveries = deliveries.drop_duplicates().copy()
print("\n======================================")
print("\nAfter removing duplicates:")
print("=====================================")
print("Matches duplicates:", matches.duplicated().sum())
print("Deliveries duplicates:", deliveries.duplicated().sum())
# ============================================================
#  UNIQUE VALUES
# ============================================================
print("\n================================================")
print("NUMBER OF UNIQUE VALUES")
print("================================================")
match_categories = [
    "city", "venue", "team1", "team2",
    "toss_winner", "toss_decision",
    "winner", "result", "player_of_match"
]

delivery_categories = [
    "batting_team", "bowling_team",
    "batsman", "bowler", "dismissal_kind"
]
print("\n================================================")
print("UNIQUE VALUES")
print("====================================================")
print("\nUNIQUE VALUES - MATCHES")
for column in match_categories:
    if column in matches.columns:
        values = sorted(matches[column].dropna().astype(str).unique())
        print(f"\n{column} — {len(values)} unique values")
        print(values)

print("\nUNIQUE VALUES - DELIVERIES")
for column in delivery_categories:
    if column in deliveries.columns:
        values = sorted(deliveries[column].dropna().astype(str).unique())
        print(f"\n{column} — {len(values)} unique values")
        if column in ["batsman", "bowler"]:
            print("Sample:", values[:20])
        else:
            print(values)
            match_team_columns = ["team1", "team2", "winner", "toss_winner"]
delivery_team_columns = ["batting_team", "bowling_team"]

match_teams = set()
for column in match_team_columns:
    if column in matches.columns:
        match_teams.update(
            matches[column].dropna().astype(str).str.strip().unique()
        )

delivery_teams = set()
for column in delivery_team_columns:
    if column in deliveries.columns:
        delivery_teams.update(
            deliveries[column].dropna().astype(str).str.strip().unique()
        )

print("Team names in matches.csv:")
print(sorted(match_teams))

print("\nTeam names in deliveries.csv:")
print(sorted(delivery_teams))

print("\nTeam names found in only one file:")
print("Only in matches:", sorted(match_teams - delivery_teams))
print("Only in deliveries:", sorted(delivery_teams - match_teams))
print("Missing values BEFORE handling:")
print("Matches:\n", matches.isna().sum())
print("Deliveries:\n", deliveries.isna().sum())

# City is useful for grouping; label missing city explicitly
if "city" in matches.columns:
    matches["city"] = matches["city"].fillna("Unknown")

# Remove only rows missing essential identifiers/analysis fields
match_required = [
    column for column in ["id", "season"]
    if column in matches.columns
]
delivery_required = [
    column for column in ["match_id", "inning", "total_runs"]
    if column in deliveries.columns
]
matches_before = len(matches)
deliveries_before = len(deliveries)

matches = matches.dropna(subset=match_required).copy()
deliveries = deliveries.dropna(subset=delivery_required).copy()

print("\nRows removed for missing essential fields:")
print("Matches:", matches_before - len(matches))
print("Deliveries:", deliveries_before - len(deliveries))

print("\nMissing values AFTER handling:")
print("Matches:\n", matches.isna().sum())
print("Deliveries:\n", deliveries.isna().sum())
#===================================================
# Convert date columns into the correct date format
# ==================================================
matches["date"] = pd.to_datetime(matches["date"], errors="coerce")
matches["season"] = matches["date"].dt.year

print("Date column type:", matches["date"].dtype)
print(matches["date"].head())
# =======================================================
# Check the cleaned datasets again
# =====================================================
for name, data in [("MATCHES", matches), ("DELIVERIES", deliveries)]:
    print(f"\n--- {name}: CLEANED DATA CHECK ---")
    print("Shape:", data.shape)
    print("Duplicate rows:", data.duplicated().sum())

    print("\nColumn data types:")
    print(data.dtypes)

    print("\nMissing values:")
    print(data.isna().sum())

    print("\nFirst 5 rows:")
    print(data.head().to_string(index=False))

print("\nMatch date type:", matches["date"].dtype)
# Save cleaned datasets as CSV files
matches.to_csv("matches_cleaned.csv", index=False)
deliveries.to_csv("deliveries_cleaned.csv", index=False)

print("Cleaned CSV files saved successfully.")
ipl_cleaned = pd.merge(
    deliveries,
    matches,
    on="id",
    how="left",
    suffixes=("_delivery", "_match")
)

ipl_cleaned.to_csv("Dataset/IPL_Cleaned.csv", index=False)
print("IPL_Cleaned.csv saved in Dataset folder")
# Exclude super-over deliveries from regular scoring analysis
analysis_deliveries = deliveries.copy()

if "is_super_over" in analysis_deliveries.columns:
    analysis_deliveries = analysis_deliveries[
        pd.to_numeric(
            analysis_deliveries["is_super_over"], errors="coerce"
        ).fillna(0) == 0
    ]
#========================================================
#  Total matches
# =====================================================
total_matches = matches["id"].nunique()
print("\nTOTAL MATCHES:", total_matches)
# =======================================================
#  Matches played in each season
# ======================================================
matches_by_season = matches.groupby("season")["id"].nunique().sort_index()
print("\n MATCHES BY SEASON:\n", matches_by_season)
#===================================================
# Completed matches with a known winner
# ====================================================
completed = matches[matches["winner"].notna()].copy()
completed = completed[completed["winner"].astype(str).str.lower() != "unknown"]
# =======================================
#  Wins by team
wins_by_team = completed["winner"].value_counts()
print("\n WINS BY TEAM:\n", wins_by_team)

# Include teams with zero wins when finding the lowest
all_teams = set(matches["team1"].dropna()) | set(matches["team2"].dropna())
wins_all_teams = wins_by_team.reindex(sorted(all_teams), fill_value=0)
#======================================
#   Highest wins
# =====================================
highest_wins = np.max(wins_all_teams.to_numpy())
print("\nTEAM(S) WITH HIGHEST WINS:")
print(wins_all_teams[wins_all_teams == highest_wins])
#=================================================
#  Lowest wins
# ==================================================
lowest_wins = np.min(wins_all_teams.to_numpy())
print("\nTEAM(S) WITH LOWEST WINS:")
print(wins_all_teams[wins_all_teams == lowest_wins])
# ======================================================
# Most Player of the Match awards
# ======================================================
print("\n MOST PLAYER-OF-THE-MATCH AWARDS:\n",
      matches["player_of_match"].value_counts().head(10))
#=========================================================
#  Most frequently used venue
# ===========================================================
print("\n MOST USED VENUES:\n", matches["venue"].value_counts().head(10))
#========================================================
#  Toss decisions
# ========================================================
print("\n TOSS DECISIONS:\n", matches["toss_decision"].value_counts())
#=======================================
#  Toss winner also won the match
# ================================================
toss_data = matches[
    matches["toss_winner"].notna() & matches["winner"].notna()
].copy()
toss_data = toss_data[
    (toss_data["toss_winner"].astype(str).str.lower() != "unknown")
    & (toss_data["winner"].astype(str).str.lower() != "unknown")
]

toss_data["toss_result"] = np.where(
    toss_data["toss_winner"] == toss_data["winner"],
    "Won match",
    "Lost match"
)

toss_wins = (toss_data["toss_result"] == "Won match").sum()
toss_percentage = 100 * toss_wins / len(toss_data) if len(toss_data) else 0

print("\n TOSS WINNERS WHO ALSO WON:", toss_wins)
print("PERCENTAGE:", round(toss_percentage, 2), "%")
print("\n TOSS RESULT COUNTS:\n", toss_data["toss_result"].value_counts())
print("\nTOSS RESULT PERCENTAGES:\n",
      toss_data["toss_result"].value_counts(normalize=True).mul(100).round(2))

# =======================================
#  Largest winning margins
# ==============================================
matches["result_margin"] = pd.to_numeric(
    matches["result_margin"], errors="coerce"
)



#=======================================
# Highest winning margin by runs
# ======================================
run_wins = matches[
    matches["result"].astype(str).str.lower().eq("runs")
]
if not run_wins.empty:
    highest_runs = np.nanmax(run_wins["result_margin"].to_numpy())
    print("HIGHEST WIN BY RUNS:")
    print(run_wins.loc[
        run_wins["result_margin"] == highest_runs,
        ["winner", "result_margin"]
    ])
 # ==================================================
# Highest winning margin by wickets
# ===========================================
wicket_wins = matches[
    matches["result"].astype(str).str.lower().eq("wickets")
]
if not wicket_wins.empty:
    highest_wickets = np.nanmax(wicket_wins["result_margin"].to_numpy())
    print("\nHIGHEST WIN BY WICKETS:")
    print(wicket_wins.loc[
        wicket_wins["result_margin"] == highest_wickets,
        ["winner", "result_margin"]
    ])
# ============================================
#  Individual innings score and top 10 total run scorers
#=======================================================
# Highest individual innings score and top 10 total run scorers
if {"batsman", "batsman_runs"}.issubset(analysis_deliveries.columns):
    innings_scores = (
        analysis_deliveries
        .groupby(["id", "inning", "batsman"])["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nHIGHEST INDIVIDUAL INNINGS SCORE:\n")
    print(innings_scores.head(1))

    runs_by_batter = (
        analysis_deliveries.groupby("batsman")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\nTOP 10 BATSMAN BY TOTAL RUNS:")
    print(runs_by_batter.head(10))
#=====================================================
#  Wickets credited to bowlers and top 10 bowlers
# =====================================================
valid_bowler_dismissals = [
    "bowled", "caught", "caught and bowled",
    "lbw", "stumped", "hit wicket"
]

if {"bowler", "dismissal_kind"}.issubset(analysis_deliveries.columns):
    credited_wickets = analysis_deliveries[
        analysis_deliveries["dismissal_kind"]
        .astype(str).str.lower().str.strip()
        .isin(valid_bowler_dismissals)
    ]

    wickets_by_bowler = credited_wickets["bowler"].value_counts()

    print("\n30. HIGHEST WICKETS BY A BOWLER:\n",
          wickets_by_bowler.head(1))
    print("\n32. TOP 10 BOWLERS BY WICKETS:\n",
          wickets_by_bowler.head(10))

# Add season to delivery rows using the match ID
season_lookup = matches.drop_duplicates("id").set_index("id")["season"]
print("Delivery columns:", analysis_deliveries.columns.tolist())
analysis_deliveries["season"] = analysis_deliveries["id"].map(season_lookup)

# 33. Season-wise total runs
runs_by_season = (
    analysis_deliveries.groupby("season")["total_runs"]
    .sum()
    .sort_index()
)
print("\n TOTAL RUNS BY SEASON:\n", runs_by_season)

#======================================================
#  Season-wise wickets/dismissals
#===========================================
if "player_dismissed" in analysis_deliveries.columns:
    wickets_by_season = (
        analysis_deliveries[analysis_deliveries["player_dismissed"].notna()]
        .groupby("season")["player_dismissed"]
        .count()
        .sort_index()
    )
    print("\n WICKETS/DISMISSALS BY SEASON:\n", wickets_by_season)

# ============================================
#  Average runs per match
#=================================================
runs_per_match = analysis_deliveries.groupby("id")["total_runs"].sum()
average_runs_per_match = runs_per_match.mean()
print("\n AVERAGE RUNS PER MATCH:", round(average_runs_per_match, 2))

# ==========================================
# Team-wise average runs per innings
#============================================
innings_totals = (
    analysis_deliveries
    .groupby(["id", "inning", "batting_team"])["total_runs"]
    .sum()
    .reset_index()
)
team_average_runs = (
    innings_totals.groupby("batting_team")["total_runs"]
    .mean()
    .sort_values(ascending=False)
)
print("\n TEAM-WISE AVERAGE RUNS PER INNINGS:\n",
      team_average_runs.round(2))

# ============================================
#  Season-wise team performance
#  ================================================
team1 = matches[["season", "team1", "winner"]].rename(
    columns={"team1": "team"}
)
team2 = matches[["season", "team2", "winner"]].rename(
    columns={"team2": "team"}
)
participations = pd.concat([team1, team2], ignore_index=True)
participations["won"] = participations["team"] == participations["winner"]

season_team_performance = (
    participations.groupby(["season", "team"])
    .agg(matches_played=("team", "size"), wins=("won", "sum"))
)
season_team_performance["win_percentage"] = (
    100 * season_team_performance["wins"]
    / season_team_performance["matches_played"]
)
print("\nSEASON-WISE TEAM PERFORMANCE:\n",
      season_team_performance.round(2))

#===============================================
#  Most successful venue for each team
# =================================================
if "venue" in completed.columns:
    venue_wins = (
        completed.dropna(subset=["venue"])
        .groupby(["winner", "venue"])
        .size()
        .reset_index(name="wins")
        .sort_values("wins", ascending=False)
        .drop_duplicates("winner")
    )
    print("\n MOST SUCCESSFUL VENUE FOR EACH TEAM:\n", venue_wins)

# =======================================
#  Major trends from the results
# ==========================================
print("\n MAJOR TRENDS")
if not matches_by_season.empty:
    print("Season with most matches:",
          matches_by_season.idxmax(), "-", matches_by_season.max(), "matches")
if not wins_by_team.empty:
    print("Team with most wins:",
          wins_by_team.index[0], "-", wins_by_team.iloc[0], "wins")
if not runs_by_season.empty:
    print("Season with most runs:",
          runs_by_season.idxmax(), "-", runs_by_season.max(), "runs")
print("Toss winners also won", round(toss_percentage, 2),
      "% of matches with a known toss winner and match winner.")

import os

sns.set_theme(style="whitegrid")

# Charts ni python/visualizations folder lo save chestundi
chart_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "visualizations"
)
os.makedirs(chart_folder, exist_ok=True)

def save_chart(fig, filename):
    fig.tight_layout()
    fig.savefig(os.path.join(chart_folder, filename), dpi=150)
    plt.close(fig)


# 1. Matches played by season
season_matches = matches.groupby("season")["id"].nunique().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=season_matches.index.astype(str), y=season_matches.values, ax=ax)
ax.set(title="Matches Played by Season", xlabel="Season", ylabel="Matches")
ax.tick_params(axis="x", rotation=45)
save_chart(fig, "01_matches_by_season.png")


# 2. Matches won by team
team_wins = matches["winner"].value_counts()
fig, ax = plt.subplots(figsize=(11, 6))
sns.barplot(x=team_wins.values, y=team_wins.index, ax=ax)
ax.set(title="Matches Won by Team", xlabel="Wins", ylabel="Team")
save_chart(fig, "02_matches_won_by_team.png")


# 3. Top 10 run scorers
top_batters = (
    analysis_deliveries.groupby("batsman")["batsman_runs"]
    .sum().sort_values(ascending=False).head(10)
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_batters.values, y=top_batters.index, ax=ax)
ax.set(title="Top 10 Run Scorers", xlabel="Runs", ylabel="Batter")
save_chart(fig, "03_top_10_batters.png")


# 4. Top 10 wicket takers
valid_dismissals = [
    "bowled", "caught", "caught and bowled", "lbw",
    "stumped", "hit wicket"
]
wicket_data = analysis_deliveries[
    analysis_deliveries["dismissal_kind"]
    .astype(str).str.lower().str.strip().isin(valid_dismissals)
]
top_bowlers = wicket_data["bowler"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, ax=ax)
ax.set(title="Top 10 Wicket Takers", xlabel="Wickets", ylabel="Bowler")
save_chart(fig, "04_top_10_bowlers.png")


# 5. Player of the Match awards
top_awards = matches["player_of_match"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_awards.values, y=top_awards.index, ax=ax)
ax.set(title="Most Player of the Match Awards", xlabel="Awards", ylabel="Player")
save_chart(fig, "05_player_awards.png")


# 6. Toss decision distribution
toss_counts = matches["toss_decision"].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(toss_counts.values, labels=toss_counts.index, autopct="%1.1f%%")
ax.set_title("Toss Decision Distribution")
save_chart(fig, "06_toss_decisions.png")


# 7. Matches won after winning the toss
toss_won_match = matches["toss_winner"] == matches["winner"]
toss_result = toss_won_match.value_counts().reindex([True, False], fill_value=0)
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(
    x=["Won toss and match", "Won toss, lost match"],
    y=toss_result.values,
    ax=ax
)
ax.set(title="Match Result After Winning the Toss", ylabel="Matches", xlabel="")
ax.tick_params(axis="x", rotation=15)
save_chart(fig, "07_toss_and_match_wins.png")


# 8. Season-wise total runs
runs_season = analysis_deliveries.groupby("season")["total_runs"].sum().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=runs_season.index, y=runs_season.values, marker="o", ax=ax)
ax.set(title="Season-wise Total Runs", xlabel="Season", ylabel="Runs")
save_chart(fig, "08_runs_by_season.png")


# 9. Season-wise wickets
dismissals = analysis_deliveries[
    analysis_deliveries["player_dismissed"].notna()
]
wickets_season = dismissals.groupby("season").size().sort_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=wickets_season.index, y=wickets_season.values, marker="o", ax=ax)
ax.set(title="Season-wise Total Wickets", xlabel="Season", ylabel="Wickets")
save_chart(fig, "09_wickets_by_season.png")


# 10. Runs distribution per match
match_runs = analysis_deliveries.groupby("id")["total_runs"].sum()
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(match_runs, bins=25, kde=True, ax=ax)
ax.set(title="Runs Distribution per Match", xlabel="Match Total Runs", ylabel="Count")
save_chart(fig, "10_runs_distribution.png")


# 11. Team performance comparison: total runs scored
team_runs = (
    analysis_deliveries.groupby("batting_team")["total_runs"]
    .sum().sort_values(ascending=False).head(10)
)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=team_runs.values, y=team_runs.index, ax=ax)
ax.set(title="Team Performance: Total Runs", xlabel="Runs", ylabel="Team")
save_chart(fig, "11_team_performance.png")


# 12. Venue-wise match count
venue_counts = matches["venue"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(11, 6))
sns.barplot(x=venue_counts.values, y=venue_counts.index, ax=ax)
ax.set(title="Top Venues by Match Count", xlabel="Matches", ylabel="Venue")
save_chart(fig, "12_venue_match_count.png")


# 13. Runs vs wickets per innings
innings_summary = analysis_deliveries.groupby(["id", "inning"]).agg(
    runs=("total_runs", "sum"),
    wickets=("player_dismissed", "count")
).reset_index()
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=innings_summary, x="runs", y="wickets", ax=ax)
ax.set(title="Runs vs Wickets per Innings", xlabel="Runs", ylabel="Wickets")
save_chart(fig, "13_runs_vs_wickets.png")


# 14. Correlation heatmap
numeric_columns = [
    column for column in
    ["over", "ball", "batsman_runs", "extra_runs", "total_runs"]
    if column in analysis_deliveries.columns
]
correlation = analysis_deliveries[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap")
save_chart(fig, "14_correlation_heatmap.png")

print(f"14 charts saved in: {chart_folder}")




