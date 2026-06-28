```markdown
# tech-spec.md

## Stack
- **Language**: TypeScript
- **Framework**: Node.js with Express for the backend; React for the frontend
- **Runtime**: Docker containers for microservices deployment

## Hosting
- **Free-tier-first**: 
  - Vercel for frontend hosting (supports serverless functions)
  - Heroku for backend hosting (free tier available)
  - MongoDB Atlas for database (free tier available)
  
## Data Model
### Collections
1. **Users**
   - `userId`: String (Primary Key)
   - `username`: String
   - `email`: String
   - `passwordHash`: String
   - `createdAt`: Date
   - `updatedAt`: Date

2. **Codebases**
   - `codebaseId`: String (Primary Key)
   - `userId`: String (Foreign Key)
   - `repositoryUrl`: String
   - `language`: String
   - `createdAt`: Date
   - `updatedAt`: Date

3. **Insights**
   - `insightId`: String (Primary Key)
   - `codebaseId`: String (Foreign Key)
   - `explanation`: String
   - `lineNumber`: Number
   - `createdAt`: Date

4. **UserPreferences**
   - `preferenceId`: String (Primary Key)
   - `userId`: String (Foreign Key)
   - `theme`: String
   - `fontSize`: Number
   - `createdAt`: Date

## API Surface
1. **User Registration**
   - **Method**: POST
   - **Path**: `/api/users/register`
   - **Purpose**: Register a new user

2. **User Login**
   - **Method**: POST
   - **Path**: `/api/users/login`
   - **Purpose**: Authenticate user and return JWT token

3. **Add Codebase**
   - **Method**: POST
   - **Path**: `/api/codebases`
   - **Purpose**: Add a new codebase for the user

4. **Get Codebase Insights**
   - **Method**: GET
   - **Path**: `/api/codebases/{codebaseId}/insights`
   - **Purpose**: Retrieve insights for a specific codebase

5. **Update User Preferences**
   - **Method**: PATCH
   - **Path**: `/api/users/preferences`
   - **Purpose**: Update user-specific preferences

6. **Get User Codebases**
   - **Method**: GET
   - **Path**: `/api/users/{userId}/codebases`
   - **Purpose**: Retrieve all codebases associated with the user

7. **Delete Codebase**
   - **Method**: DELETE
   - **Path**: `/api/codebases/{codebaseId}`
   - **Purpose**: Remove a codebase from the user's account

## Security Model
- **Authentication**: JWT (JSON Web Tokens) for user sessions
- **Secrets Management**: Use environment variables for sensitive information (e.g., database URIs, API keys)
- **IAM**: Role-based access control (RBAC) for user permissions (e.g., admin vs. regular user)

## Observability
- **Logs**: Use Winston for logging application events and errors
- **Metrics**: Integrate Prometheus for collecting metrics on API usage and performance
- **Traces**: Use OpenTelemetry for distributed tracing to monitor request flows and identify bottlenecks

## Build/CI
- **Build Tool**: Webpack for bundling frontend assets
- **CI/CD**: GitHub Actions for continuous integration and deployment
  - **Build Steps**: Linting, testing, building Docker images
  - **Deployment Steps**: Push to Heroku and Vercel upon successful build
```
