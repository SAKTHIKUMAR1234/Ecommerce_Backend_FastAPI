from contextvars import ContextVar

  
current_user: ContextVar[dict] = ContextVar('current_user')

def set_current_user(activity) -> None:
  
  current_user.set({
    'email' : activity.user.email,
    'session_id' : activity.session_id,
    'role' : activity.user.role
  })
  
def get_current_user():
  
  return current_user.get()