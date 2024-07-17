# Jira Slack Auto
This package was developed by mwcha because configure about autonomous system with API

### STEP 1
a
### STEP 2
b
### STEP 3
Run it
### Tip
abc

## Dependencies

This package depends on the following ROS 2 packages:

- requests
- slack_sdk
```bash
cd /{workspace}/src
pip install -r requirements_pkg.txt
```

Make sure to have these packages installed in your ROS 2 environment before using `topic_checker`.

## Installation

1. Clone the repository into your ROS2 workspace's `src` director

```bash
cd /{workspace}/src
git clone https://github.com/minwoo1213/Jira_Slack_Auto.git
```

2. Build the package using colcon

```bash
cd /{workspace}/
colcon build
```

3. Source the setup script to add the package to your ROS 2 environment

```bash
source /{workspace}/install/local_setup.bash
```

4. Launch your package

```bash
python jira_slack_integration.py
```
