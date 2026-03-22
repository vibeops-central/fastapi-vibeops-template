# Skill: CRUD Resources

> Load this skill when: building standard create/read/update/delete resources, paginated lists, or repository + service patterns.

---

## Layered Pattern

```
Router (HTTP only)
  └── Service (business logic)
        └── Repository (DB queries)
              └── Model (SQLAlchemy)
```

### Repository
- DB queries only — no business logic
- Returns domain objects (model instances), not raw rows
- Async methods using SQLAlchemy 2.0 `select()` style

```python
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> User:
        user = User(**data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
```

### Service
- All business logic lives here
- Calls repositories — never accesses models directly
- Raises domain exceptions from `src/core/exceptions.py`

### Pagination
- Standard pattern: `skip` + `limit` query params
- Default: `skip=0`, `limit=20`, max `limit=100`
- Always return total count alongside results

## Known Gotchas

- **Async pitfall:** Never use `time.sleep()` in async code — use `await asyncio.sleep()`
- **Pydantic v2:** Use `model_validate()` not `parse_obj()`, `model_dump()` not `dict()`
- **Redis cache keys:** Follow pattern `{resource}:{id}:{version}` — do not invent new patterns
- **CORS:** `ALLOWED_ORIGINS` must be set explicitly in production — `*` is only for local dev

## Checklist (append to self-review)

- [ ] Repository handles all DB access — no direct model access in services
- [ ] Service owns all business logic — no logic in routers
- [ ] Pagination implemented for list endpoints
- [ ] `response_model` declared on all endpoints
- [ ] Custom exceptions used — no raw `HTTPException` in services
