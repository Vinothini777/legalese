# Phase 5: Testing Phase

Project: LegalEase - AI Legal Document Assistant

## Testing Types Performed:

### 1. Unit Testing:
- Tested user registration API with valid/invalid data
- Tested login with correct/wrong password
- Tested Gemini API response for legal queries
- Result: All APIs working

### 2. Integration Testing:
- Frontend to Backend connection tested
- Chatbot flow: User question -> Backend -> Gemini -> Answer displayed
- Document flow: Form fill -> PDF generated -> Download works
- Result: Integration successful

### 3. Functional Testing:
- Test Case 1: User can register and login - PASS
- Test Case 2: Chatbot answers legal questions - PASS
- Test Case 3: Rental Agreement PDF is generated correctly - PASS
- Test Case 4: Dashboard shows chat history - PASS

### 4. UI Testing:
- Checked responsiveness on mobile and desktop
- Checked buttons, forms, navigation links
- Result: UI responsive

### 5. Security Testing:
- JWT token validation tested
- Unauthorized access blocked
- Passwords stored as hash

## Tools Used:
- Manual Testing
- Postman for API testing
- Browser DevTools

## Conclusion: Application is stable and ready for deployment.
