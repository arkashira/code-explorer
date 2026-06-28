# partner-targets.md

## Partner Integration Roadmap for Code Explorer

### Target Integrations

| Partner/SaaS/API                | Free Tier Limits                       | Integration Effort | Value-Add (User Job Solved)                                    | Affiliate/Revenue-Share Potential |
|----------------------------------|---------------------------------------|--------------------|----------------------------------------------------------------|-----------------------------------|
| GitHub API                       | 5,000 requests/month                  | M                  | Enables seamless access to repositories and code history, enhancing navigation and insights. | Yes                               |
| Slack API                        | Up to 10,000 messages/month           | S                  | Facilitates team communication and collaboration around codebase insights. | Yes                               |
| JIRA API                         | 10 users, 2GB storage                 | M                  | Integrates project management with code insights, improving task tracking related to code changes. | Yes                               |
| Snyk API                        | 200 tests/month                       | M                  | Enhances security insights for codebases, addressing vulnerabilities in real-time. | Yes                               |
| CircleCI API                     | 2,500 build minutes/month             | L                  | Provides CI/CD insights, helping developers understand deployment contexts of code changes. | Yes                               |
| Trello API                       | 10 boards, 10MB per attachment        | S                  | Allows project tracking and task management linked to codebase insights. | No                                |
| Figma API                        | 3 projects, 30 days of version history| M                  | Enables design and code collaboration, linking design specs to codebase understanding. | No                                |
| Notion API                       | 1,000 blocks                          | S                  | Facilitates documentation and knowledge sharing around code insights, improving team learning. | No                                |

### Rationale for Selection

1. **GitHub API**: As the primary platform for code hosting, integrating with GitHub allows Code Explorer to pull in repository data, commit history, and pull requests, which are essential for understanding codebases.

2. **Slack API**: Communication is key in software development. Integrating with Slack allows users to share insights and explanations directly within their team’s communication channels, enhancing collaboration.

3. **JIRA API**: Many development teams use JIRA for project management. By integrating with JIRA, Code Explorer can link code insights to specific tasks or issues, providing context that helps developers prioritize their work.

4. **Snyk API**: Security is a top concern for developers. Integrating Snyk allows Code Explorer to provide security insights directly related to the code being analyzed, addressing a critical user job.

5. **CircleCI API**: Continuous integration and deployment are integral to modern development workflows. Integrating with CircleCI helps users understand how changes in the codebase affect the build and deployment processes.

6. **Trello API**: While not as robust as JIRA, Trello is popular among smaller teams. Integrating with Trello allows users to track tasks and link them to code insights, improving overall project visibility.

7. **Figma API**: For teams that work closely with design, integrating Figma can bridge the gap between design and development, allowing for a more cohesive understanding of how design decisions impact the codebase.

8. **Notion API**: Notion is widely used for documentation. Integrating with Notion can help teams document their codebase insights and explanations, fostering a culture of knowledge sharing and continuous learning.

### Prioritization Criteria

- **Affiliate/Revenue-Share Potential**: Prioritized partners that offer affiliate programs or revenue-sharing models to enhance monetization opportunities.
- **Integration Effort**: Focused on a mix of medium and small effort integrations to ensure a balanced roadmap that can be executed efficiently.
- **Value-Add**: Each integration directly addresses a specific user job, ensuring that the partnerships enhance the overall value proposition of Code Explorer.