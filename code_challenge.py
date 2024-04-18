# Import necessary libraries
import requests
from datetime import datetime, timedelta

# Function to get pull requests from a GitHub repository
def get_pull_requests(user, repo):
    # Construct the URL for the GitHub API
    url = f"https://api.github.com/repos/{user}/{repo}/pulls"
    # Set the headers to accept the GitHub v3 API
    headers = {'Accept': 'application/vnd.github.v3+json'}
    # Send a GET request to the GitHub API
    response = requests.get(url, headers=headers)
    # If the response status code is not 200 (OK), return None
    if response.status_code != 200:
        return None
    # Otherwise, return the JSON response
    return response.json()

# Function to filter pull requests that were opened or closed in the last week
def filter_pull_requests(pull_requests):
    # Get the datetime for one week ago
    week_ago = datetime.now() - timedelta(days=7)
    # Initialize lists to store opened and closed pull requests
    opened = []
    closed = []
    # Loop through all pull requests
    for pr in pull_requests:
        # Convert the created_at string to a datetime object
        created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        # If the pull request was created in the last week
        if created_at > week_ago:
            # If the pull request is open, add it to the opened list
            if pr['state'] == 'open':
                opened.append(pr)
            # Otherwise, add it to the closed list
            else:
                closed.append(pr)
    # Return the lists of opened and closed pull requests
    return opened, closed

# Function to print an email summary report
def print_email_summary(user, repo, opened, closed):
    # Print the From, To, and Subject lines of the email
    print(f"From: no-reply@github.com")
    print(f"To: benjaminsaullmcculloch@gmail.com")
    print(f"Subject: Weekly Pull Request Summary for {user}/{repo}")
    # Print the body of the email
    print("\nBody:")
    print(f"In the last week, there have been {len(opened)} opened and {len(closed)} closed pull requests in the {user}/{repo} repository.")
    print("\nOpened Pull Requests:")
    # Loop through all opened pull requests and print their titles
    for pr in opened:
        print(f"- {pr['title']}")
    print("\nClosed Pull Requests:")
    # Loop through all closed pull requests and print their titles
    for pr in closed:
        print(f"- {pr['title']}")

# Main function to run the script
def main():
    # Set the GitHub username and repository name
    user = 'Benjamin-Saul-1989'  # GitHub username
    repo = 'Benjamin-Saul-1989.github.io'  # GitHub repository name
    # Get all pull requests from the repository
    pull_requests = get_pull_requests(user, repo)
    # If no pull requests were retrieved, print an error message and return
    if pull_requests is None:
        print(f"Could not retrieve pull requests for {user}/{repo}")
        return
    # Filter the pull requests that were opened or closed in the last week
    opened, closed = filter_pull_requests(pull_requests)
    # Print an email summary report
    print_email_summary(user, repo, opened, closed)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
