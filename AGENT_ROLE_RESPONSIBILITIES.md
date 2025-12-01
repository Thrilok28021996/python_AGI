# Agent Role Responsibilities

**A guide to what each agent role should and shouldn't do**

---

## 🎯 Overview

This document clarifies the responsibilities of each agent role, specifically **who writes code and who doesn't**, mirroring real-world company roles.

---

## 📊 Quick Reference Table

| Role | Writes Code? | What They Produce | Real-World Equivalent |
|------|-------------|-------------------|----------------------|
| **CEO** | ❌ No | Strategic decisions, vision, approvals | Company CEO |
| **Product Manager** | ❌ No | Requirements, user stories, PRDs | Product Manager |
| **Lead Developer** | ✅ Yes | Architecture code, system design | Tech Lead |
| **Backend Developer** | ✅ Yes | Server-side code, APIs, databases | Backend Engineer |
| **Frontend Developer** | ✅ Yes | UI code, components, client logic | Frontend Engineer |
| **QA Tester** | ⚠️ Optional | Test plans, test code (optional) | QA Engineer |
| **DevOps Engineer** | ✅ Yes | Infrastructure code, CI/CD scripts | DevOps Engineer |
| **UI/UX Designer** | ❌ No | Wireframes, designs, specs | UI/UX Designer |
| **Security Expert** | ❌ No | Security analysis, recommendations | Security Analyst |
| **Technical Writer** | ❌ No | Documentation, guides, API docs | Technical Writer |

---

## 👥 Detailed Role Breakdown

### 1. CEO

**Real-World Role:** Company Chief Executive Officer

**Responsibilities:**
- Define project vision and goals
- Make high-level strategic decisions
- Approve major changes
- Resolve conflicts between team members
- Set priorities

**What They Produce:**
- ✅ Strategic plans
- ✅ Vision statements
- ✅ Approval/rejection decisions
- ✅ Priority lists
- ❌ **NO CODE**

**Example Output:**
```
Role: CEO
Response:
Approved the user authentication feature. This aligns with our Q1 security goals.

Analysis:
This feature addresses our main customer concern about data security.

Recommendation:
- Prioritize this over the analytics dashboard
- Allocate 2 developers for 2 weeks
- Target launch for end of month

Questions/Concerns:
None - proceed with implementation.
```

---

### 2. Product Manager

**Real-World Role:** Product Manager (PM)

**Responsibilities:**
- Define product requirements
- Create user stories
- Prioritize features
- Coordinate between technical and business teams
- Ensure product meets user needs

**What They Produce:**
- ✅ Product Requirements Documents (PRDs)
- ✅ User stories
- ✅ Feature specifications
- ✅ Acceptance criteria
- ❌ **NO CODE**

**Example Output:**
```
Role: Product Manager
Response:
User Story: As a user, I want to register with email/password
so that I can create a secure account.

Analysis:
This is a core feature needed before any other functionality.
Users expect standard email registration.

Recommendation:
Acceptance Criteria:
- Email validation (format check)
- Password strength requirements (8+ chars, 1 number)
- Confirmation email sent
- Account created in database
- User redirected to dashboard

Questions/Concerns:
Do we need social login (Google/Facebook) in v1?
```

---

### 3. Lead Developer

**Real-World Role:** Technical Lead / Engineering Manager

**Responsibilities:**
- Design system architecture
- Write high-quality code
- Review code from other developers
- Make technical decisions
- Ensure code quality and best practices

**What They Produce:**
- ✅ **ARCHITECTURAL CODE**
- ✅ System design diagrams (as code comments)
- ✅ Code review feedback
- ✅ Technical standards

**Example Output:**
```
Role: Lead Developer
Response:
Here's the architecture for the user registration system.

Analysis:
We'll use a 3-layer architecture: API → Service → Repository

Recommendation:
```python
# src/architecture/layers.py
from fastapi import FastAPI
from pydantic import BaseModel

# API Layer
class UserRegistrationRequest(BaseModel):
    email: str
    password: str

# Service Layer
class UserService:
    def register_user(self, email: str, password: str):
        # Hash password
        # Validate email
        # Call repository
        pass

# Repository Layer
class UserRepository:
    def create_user(self, user_data: dict):
        # Database insertion
        pass
```

Questions/Concerns:
Should we use SQLAlchemy or raw SQL for the repository layer?
```

---

### 4. Backend Developer

**Real-World Role:** Backend Engineer / Server-Side Developer

**Responsibilities:**
- Implement server-side logic
- Create and manage APIs
- Design and manage databases
- Ensure backend performance and security
- Write backend tests

**What They Produce:**
- ✅ **SERVER-SIDE CODE** (Python, Node.js, etc.)
- ✅ API endpoints
- ✅ Database schemas
- ✅ Business logic implementation

**Example Output:**
```
Role: Backend Developer
Response:
Implemented the user registration endpoint.

Analysis:
Used FastAPI with Pydantic for validation and bcrypt for password hashing.

Recommendation:
```python
# src/api/users.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import bcrypt
from database import db

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@app.post("/register")
async def register_user(user: UserCreate):
    # Check if user exists
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(400, "Email already registered")

    # Hash password
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    # Create user
    result = await db.users.insert_one({
        "email": user.email,
        "password": hashed,
        "created_at": datetime.now()
    })

    return {"id": str(result.inserted_id), "email": user.email}
```

Questions/Concerns:
Should we send confirmation email in this endpoint or async job?
```

---

### 5. Frontend Developer

**Real-World Role:** Frontend Engineer / UI Developer

**Responsibilities:**
- Implement user interfaces
- Ensure responsive design
- Optimize frontend performance
- Integrate with backend APIs
- Write frontend tests

**What They Produce:**
- ✅ **CLIENT-SIDE CODE** (React, Vue, vanilla JS, HTML, CSS)
- ✅ UI components
- ✅ API integration code

**Example Output:**
```
Role: Frontend Developer
Response:
Created the registration form component.

Analysis:
Used React with form validation and API integration.

Recommendation:
```javascript
// src/components/RegisterForm.jsx
import React, { useState } from 'react';

function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.detail);
        return;
      }

      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (err) {
      setError('Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit">Register</button>
    </form>
  );
}
```

Questions/Concerns:
Should we add password strength indicator?
```

---

### 6. QA Tester

**Real-World Role:** QA Engineer / Test Engineer

**Responsibilities:**
- Write test cases
- Perform manual and automated testing
- Find and report bugs
- Verify bug fixes
- Ensure product quality

**What They Produce:**
- ✅ Test plans and test cases
- ⚠️ **OPTIONAL: Test code**
- ✅ Bug reports
- ✅ Quality feedback

**Example Output (with test code):**
```
Role: QA Tester
Response:
Created test cases for user registration.

Analysis:
Tested happy path, validation errors, and edge cases.

Recommendation:
Test Cases:
1. Valid registration → Success
2. Duplicate email → Error 400
3. Invalid email format → Error 422
4. Weak password → Error 422

```python
# tests/test_registration.py
import pytest

def test_valid_registration(client):
    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "SecurePass123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_duplicate_email(client):
    # Register first time
    client.post("/register", json={
        "email": "test@example.com",
        "password": "Pass123"
    })

    # Try again
    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "Pass456"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
```

Questions/Concerns:
Should we add load testing for concurrent registrations?
```

**Example Output (without test code - also valid):**
```
Role: QA Tester
Response:
Test plan for user registration feature.

Analysis:
Need to verify all validation rules and error handling.

Recommendation:
Manual Test Cases:
1. Happy Path:
   - Enter valid email: test@example.com
   - Enter valid password: SecurePass123
   - Click Register
   - Verify: User created, redirected to dashboard

2. Error Cases:
   - Invalid email format → Show error "Invalid email"
   - Password < 8 chars → Show error "Password too short"
   - Duplicate email → Show error "Email already exists"

3. Edge Cases:
   - Very long email (100+ chars)
   - Special characters in password
   - Network timeout during registration

Questions/Concerns:
Do we need to test email confirmation flow?
```

---

### 7. DevOps Engineer

**Real-World Role:** DevOps Engineer / SRE

**Responsibilities:**
- Set up CI/CD pipelines
- Manage infrastructure
- Ensure deployment processes
- Monitor system performance
- Handle security and scalability

**What They Produce:**
- ✅ **INFRASTRUCTURE CODE** (Terraform, Ansible, Docker)
- ✅ **CI/CD SCRIPTS** (GitHub Actions, Jenkins)
- ✅ Configuration files
- ✅ Deployment automation

**Example Output:**
```
Role: DevOps Engineer
Response:
Created Docker configuration and GitHub Actions CI/CD pipeline.

Analysis:
Containerized the application for consistent deployments.

Recommendation:
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t myapp:latest .

      - name: Run tests
        run: docker run myapp:latest pytest

      - name: Deploy to production
        run: |
          docker tag myapp:latest registry.com/myapp:latest
          docker push registry.com/myapp:latest
```

Questions/Concerns:
Should we add staging environment before production?
```

---

### 8. UI/UX Designer

**Real-World Role:** UI/UX Designer / Product Designer

**Responsibilities:**
- Design user interfaces
- Create wireframes and mockups
- Ensure good user experience
- Design system components
- Provide design feedback

**What They Produce:**
- ✅ Wireframes and mockups (as descriptions or ASCII art)
- ✅ Design specifications
- ✅ Color schemes and typography
- ✅ User flow diagrams
- ❌ **NO CODE**

**Example Output:**
```
Role: UI/UX Designer
Response:
Registration form design specification.

Analysis:
Clean, simple design that builds trust. Follows material design principles.

Recommendation:
Layout:
┌─────────────────────────────────┐
│         LOGO                    │
│                                 │
│  Create Your Account            │
│                                 │
│  ┌─────────────────────────┐   │
│  │ Email                   │   │
│  └─────────────────────────┘   │
│                                 │
│  ┌─────────────────────────┐   │
│  │ Password                │   │
│  └─────────────────────────┘   │
│                                 │
│  [ Register Button ]            │
│                                 │
│  Already have account? Login    │
└─────────────────────────────────┘

Design Specifications:
- Background: #FFFFFF
- Primary Color: #2196F3 (blue)
- Input borders: #E0E0E0
- Input focus: #2196F3
- Button: #2196F3 with white text
- Button hover: #1976D2
- Font: Roboto, 16px for inputs
- Spacing: 16px between elements
- Max width: 400px, centered

UX Considerations:
- Show password strength indicator
- Display clear error messages below inputs
- Disable button during submission
- Show loading state
- Auto-focus email field on page load

Questions/Concerns:
Should we add social login buttons (Google/GitHub)?
```

---

### 9. Security Expert

**Real-World Role:** Security Analyst / Security Engineer

**Responsibilities:**
- Identify security vulnerabilities
- Implement security best practices
- Review code for security issues
- Ensure data protection
- Conduct security audits

**What They Produce:**
- ✅ Security analysis reports
- ✅ Vulnerability assessments
- ✅ Security recommendations
- ✅ Compliance checklists
- ❌ **NO CODE** (analysis only, not implementation)

**Example Output:**
```
Role: Security Expert
Response:
Security analysis of user registration system.

Analysis:
Several security concerns identified that need addressing.

Recommendation:
Security Issues Found:

1. CRITICAL: Password Storage
   - Risk: Passwords may not be hashed properly
   - Recommendation: Use bcrypt with cost factor 12+
   - Verify: Check if password is hashed before storage

2. HIGH: Rate Limiting
   - Risk: Brute force attacks on registration endpoint
   - Recommendation: Implement rate limiting (5 requests/minute per IP)
   - Add: CAPTCHA after 3 failed attempts

3. MEDIUM: Email Verification
   - Risk: Fake accounts, email enumeration
   - Recommendation: Send confirmation email before account activation
   - Add: Email verification token with expiration

4. MEDIUM: Input Validation
   - Risk: SQL injection, XSS attacks
   - Recommendation: Use parameterized queries, sanitize inputs
   - Verify: All inputs validated on backend

5. LOW: HTTPS
   - Risk: Credentials transmitted in plain text
   - Recommendation: Enforce HTTPS for all endpoints
   - Add: HSTS header

Security Checklist:
☐ Password hashed with bcrypt (cost 12+)
☐ Rate limiting implemented
☐ Email verification required
☐ Input validation on all fields
☐ HTTPS enforced
☐ CSRF protection enabled
☐ SQL injection prevented
☐ XSS protection in place

Questions/Concerns:
Do we need 2FA for high-risk accounts?
Should we implement account lockout after failed attempts?
```

---

### 10. Technical Writer

**Real-World Role:** Technical Writer / Documentation Engineer

**Responsibilities:**
- Write documentation
- Create API documentation
- Write user guides
- Ensure documentation clarity
- Keep documentation up-to-date

**What They Produce:**
- ✅ API documentation
- ✅ User guides
- ✅ README files
- ✅ Inline documentation
- ❌ **NO CODE**

**Example Output:**
```
Role: Technical Writer
Response:
API documentation for user registration endpoint.

Analysis:
Clear, comprehensive documentation for developers integrating with the API.

Recommendation:
# User Registration API

## POST /register

Register a new user account.

### Request

**Endpoint:** `POST /api/register`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address (max 255 chars) |
| password | string | Yes | Password (min 8 chars, must include number) |

### Response

**Success (200 OK):**
```json
{
  "id": "user_123abc",
  "email": "user@example.com",
  "created_at": "2025-11-30T10:00:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

**Error (422 Validation Error):**
```json
{
  "detail": [
    {
      "field": "password",
      "message": "Password must be at least 8 characters"
    }
  ]
}
```

### Example Usage

**cURL:**
```bash
curl -X POST https://api.example.com/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'
```

**JavaScript:**
```javascript
const response = await fetch('https://api.example.com/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123'
  })
});
const data = await response.json();
```

### Notes
- Email confirmation is sent after successful registration
- Account must be verified before login
- Rate limited to 5 requests per minute per IP

Questions/Concerns:
Should we add code examples in more languages (Python, Ruby)?
```

---

## 🔧 How System Enforces Roles

### In Collaborative Workflows

The system now provides **role-specific instructions** to each agent:

**For Developers:**
```
⚠️ Backend Developer: You MUST provide actual, working code in ```language blocks.
   DO NOT just discuss - WRITE COMPLETE, RUNNABLE CODE.
```

**For Product Managers:**
```
📋 Product Manager: Provide requirements, user stories, or specifications.
   NO CODE - Focus on WHAT to build, not HOW.
```

**For Designers:**
```
🎨 UI/UX Designer: Provide design specifications, wireframes, UI/UX guidance.
   NO CODE - Focus on visual design and user experience.
```

### Validation Logic

```python
# Roles that MUST produce code
code_required = ["developer", "devops"]

# Roles that should NOT produce code
no_code = ["product", "manager", "ceo", "designer", "security", "writer"]

# QA can optionally write test code
# Security analyzes but doesn't implement
```

---

## ✅ Summary

### Who Writes Code?

| Role | Code Required | Type of Code |
|------|--------------|--------------|
| **Developers** (Backend, Frontend, Lead) | ✅ **YES** | Application code |
| **DevOps** | ✅ **YES** | Infrastructure code |
| **QA Tester** | ⚠️ **Optional** | Test code |
| **Everyone Else** | ❌ **NO** | N/A |

### Real-World Alignment

This mirrors actual company structures:
- ✅ Product Managers write specs, not code
- ✅ Designers create designs, not implementations
- ✅ Security experts analyze, don't implement
- ✅ Technical writers document, don't code
- ✅ Only engineers write code

---

**Status:** ✅ Fixed in latest version
**Last Updated:** 2025-11-30
