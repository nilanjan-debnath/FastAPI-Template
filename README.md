# Implementing FastAPI best practices for Production
1. ✅ `Async` Friendly Code 
2. ⚠️ Avoid `Heavy Computation` in Endpoints
3. 🚫 Disable `Swagger` & `ReDoc` in Production
4. 🚫 Don't Manually Construct Response Model (just mentioning it in Endpoint is enough)
5. ✅ Validate user input with `Pydantic Model` (Don't use any hidden validation)
6. ✅ Use `Dependency Injection` for getting resources accessible by functions
7. ⚠️ Avoid new DB connection/session in every endpoint
8. ✅ Use `Lifespan Events` for resource management
9. ✅ Use `Config` class for managing environment variables
10. ✅ Use `logging` with modern library like Loguru/structlog
11. ✅ Add `ratelimiter` in production environment
12. ✅ Use `gunicorn` with `uvicorn.workers` for production deployment 
