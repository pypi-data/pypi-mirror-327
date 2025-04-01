from pydantic import BaseModel, field_validator

class Config(BaseModel):
    # 插件回复优先级：数值越小优先级越高，最小为1
    ai_topia_priority: int = 20

    
    
