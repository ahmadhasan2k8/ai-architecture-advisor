"""
Refactoring Templates for Design Pattern Implementation

This module provides before/after examples and transformation templates
for implementing design patterns based on the repository's examples.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from textwrap import dedent


@dataclass
class RefactoringTemplate:
    """Template for refactoring code to implement a design pattern"""
    pattern_name: str
    scenario: str
    before_code: str
    after_code: str
    explanation: str
    steps: List[str]
    considerations: List[str]
    testing_notes: str


# Refactoring templates based on repository examples
REFACTORING_TEMPLATES: Dict[str, List[RefactoringTemplate]] = {
    
    "strategy": [
        RefactoringTemplate(
            pattern_name="strategy",
            scenario="Replace if/elif chain with Strategy pattern",
            before_code=dedent("""
                def process_payment(payment_type: str, amount: float) -> str:
                    if payment_type == "credit_card":
                        # 15 lines of credit card processing
                        fee = amount * 0.03
                        return f"Credit card payment of ${amount + fee} processed"
                    elif payment_type == "paypal":
                        # 12 lines of PayPal processing  
                        fee = amount * 0.025
                        return f"PayPal payment of ${amount + fee} processed"
                    elif payment_type == "crypto":
                        # 20 lines of crypto processing
                        fee = amount * 0.01
                        return f"Crypto payment of ${amount + fee} processed"
                    else:
                        raise ValueError(f"Unknown payment type: {payment_type}")
            """).strip(),
            after_code=dedent("""
                from abc import ABC, abstractmethod
                
                class PaymentProcessor(ABC):
                    @abstractmethod
                    def process(self, amount: float) -> str:
                        pass
                
                class CreditCardProcessor(PaymentProcessor):
                    def process(self, amount: float) -> str:
                        fee = amount * 0.03
                        return f"Credit card payment of ${amount + fee} processed"
                
                class PayPalProcessor(PaymentProcessor):
                    def process(self, amount: float) -> str:
                        fee = amount * 0.025
                        return f"PayPal payment of ${amount + fee} processed"
                
                class CryptoProcessor(PaymentProcessor):
                    def process(self, amount: float) -> str:
                        fee = amount * 0.01
                        return f"Crypto payment of ${amount + fee} processed"
                
                class PaymentService:
                    def __init__(self):
                        self.processors = {
                            "credit_card": CreditCardProcessor(),
                            "paypal": PayPalProcessor(),
                            "crypto": CryptoProcessor()
                        }
                    
                    def process_payment(self, payment_type: str, amount: float) -> str:
                        processor = self.processors.get(payment_type)
                        if not processor:
                            raise ValueError(f"Unknown payment type: {payment_type}")
                        return processor.process(amount)
            """).strip(),
            explanation="Replace conditional logic with Strategy pattern when you have 3+ algorithms for the same problem",
            steps=[
                "1. Create abstract base class (PaymentProcessor) defining the interface",
                "2. Extract each conditional branch into a separate strategy class",
                "3. Create context class (PaymentService) to manage strategies",
                "4. Replace original function with strategy delegation",
                "5. Add new payment types by creating new strategy classes"
            ],
            considerations=[
                "Use when you have 3+ algorithms that are likely to change or expand",
                "Each strategy should be independently testable",
                "Consider strategy selection mechanism (registry, factory, etc.)",
                "Strategies should be stateless for thread safety"
            ],
            testing_notes="Test each strategy independently, then test strategy selection in context class"
        ),
        
        RefactoringTemplate(
            pattern_name="strategy",
            scenario="Dynamic algorithm selection based on data characteristics",
            before_code=dedent("""
                def sort_data(data: List[int]) -> List[int]:
                    if len(data) < 100:
                        # Use insertion sort for small arrays
                        return insertion_sort(data.copy())
                    elif len(data) < 10000:
                        # Use quicksort for medium arrays
                        return quicksort(data.copy())
                    else:
                        # Use merge sort for large arrays
                        return merge_sort(data.copy())
            """).strip(),
            after_code=dedent("""
                from abc import ABC, abstractmethod
                from typing import List
                
                class SortStrategy(ABC):
                    @abstractmethod
                    def sort(self, data: List[int]) -> List[int]:
                        pass
                
                class InsertionSortStrategy(SortStrategy):
                    def sort(self, data: List[int]) -> List[int]:
                        return insertion_sort(data.copy())
                
                class QuickSortStrategy(SortStrategy):
                    def sort(self, data: List[int]) -> List[int]:
                        return quicksort(data.copy())
                
                class MergeSortStrategy(SortStrategy):
                    def sort(self, data: List[int]) -> List[int]:
                        return merge_sort(data.copy())
                
                class SmartSorter:
                    def __init__(self):
                        self.strategies = {
                            'small': InsertionSortStrategy(),
                            'medium': QuickSortStrategy(),
                            'large': MergeSortStrategy()
                        }
                    
                    def sort(self, data: List[int]) -> List[int]:
                        strategy_key = self._select_strategy(len(data))
                        return self.strategies[strategy_key].sort(data)
                    
                    def _select_strategy(self, size: int) -> str:
                        if size < 100:
                            return 'small'
                        elif size < 10000:
                            return 'medium'
                        else:
                            return 'large'
            """).strip(),
            explanation="Use Strategy pattern for intelligent algorithm selection based on input characteristics",
            steps=[
                "1. Define strategy interface for the algorithm family",
                "2. Implement each algorithm as a separate strategy",
                "3. Create smart selector that chooses strategy based on input",
                "4. Make strategy selection logic configurable if needed",
                "5. Add performance monitoring to validate strategy choices"
            ],
            considerations=[
                "Strategy selection logic should be well-tested",
                "Consider caching strategy instances for performance",
                "Document the criteria for strategy selection",
                "Allow for strategy selection override when needed"
            ],
            testing_notes="Test strategy selection logic with various input sizes, benchmark performance"
        )
    ],
    
    "factory": [
        RefactoringTemplate(
            pattern_name="factory",
            scenario="Replace type-based object creation with Factory pattern",
            before_code=dedent("""
                def create_notification(notification_type: str, message: str):
                    if notification_type == "email":
                        return EmailNotification(message)
                    elif notification_type == "sms":
                        return SMSNotification(message)
                    elif notification_type == "push":
                        return PushNotification(message)
                    elif notification_type == "slack":
                        return SlackNotification(message)
                    else:
                        raise ValueError(f"Unknown notification type: {notification_type}")
                
                # Usage scattered throughout codebase
                email_notif = create_notification("email", "Hello!")
                sms_notif = create_notification("sms", "Alert!")
            """).strip(),
            after_code=dedent("""
                from abc import ABC, abstractmethod
                
                class Notification(ABC):
                    @abstractmethod
                    def send(self, message: str) -> bool:
                        pass
                
                class NotificationFactory:
                    _notification_types = {
                        "email": EmailNotification,
                        "sms": SMSNotification,
                        "push": PushNotification,
                        "slack": SlackNotification
                    }
                    
                    @classmethod
                    def create(cls, notification_type: str, **kwargs) -> Notification:
                        notification_class = cls._notification_types.get(notification_type)
                        if not notification_class:
                            raise ValueError(f"Unknown notification type: {notification_type}")
                        return notification_class(**kwargs)
                    
                    @classmethod
                    def register_type(cls, type_name: str, notification_class):
                        \"\"\"Allow registration of new notification types\"\"\"
                        cls._notification_types[type_name] = notification_class
                    
                    @classmethod
                    def available_types(cls) -> List[str]:
                        return list(cls._notification_types.keys())
                
                # Usage
                email_notif = NotificationFactory.create("email", recipient="user@example.com")
                sms_notif = NotificationFactory.create("sms", phone_number="+1234567890")
            """).strip(),
            explanation="Use Factory pattern when you need to create families of related objects",
            steps=[
                "1. Define common interface for all products (Notification)",
                "2. Create factory class with creation methods",
                "3. Register all product types in the factory",
                "4. Add extensibility mechanism for new types",
                "5. Replace direct instantiation with factory calls"
            ],
            considerations=[
                "Factory is useful when you have 3+ related classes",
                "Consider Abstract Factory for families of related products",
                "Make factory extensible for new product types",
                "Factory can handle complex construction logic"
            ],
            testing_notes="Test factory with all registered types, test error handling for unknown types"
        )
    ],
    
    "observer": [
        RefactoringTemplate(
            pattern_name="observer",
            scenario="Replace manual notification loops with Observer pattern",
            before_code=dedent("""
                class UserService:
                    def __init__(self):
                        self.email_service = EmailService()
                        self.audit_service = AuditService()
                        self.analytics_service = AnalyticsService()
                    
                    def update_user_profile(self, user_id: str, data: dict):
                        # Update user data
                        user = self.update_user_data(user_id, data)
                        
                        # Manual notifications - hard to maintain
                        self.email_service.send_profile_update_email(user)
                        self.audit_service.log_profile_update(user)
                        self.analytics_service.track_profile_update(user)
                        # If we add more services, we need to update this function
            """).strip(),
            after_code=dedent("""
                from abc import ABC, abstractmethod
                from typing import List, Any
                
                class Observer(ABC):
                    @abstractmethod
                    def update(self, event_type: str, data: Any) -> None:
                        pass
                
                class Subject:
                    def __init__(self):
                        self._observers: List[Observer] = []
                    
                    def attach(self, observer: Observer) -> None:
                        self._observers.append(observer)
                    
                    def detach(self, observer: Observer) -> None:
                        self._observers.remove(observer)
                    
                    def notify(self, event_type: str, data: Any) -> None:
                        for observer in self._observers:
                            observer.update(event_type, data)
                
                class UserService(Subject):
                    def __init__(self):
                        super().__init__()
                    
                    def update_user_profile(self, user_id: str, data: dict):
                        # Update user data
                        user = self.update_user_data(user_id, data)
                        
                        # Notify all observers
                        self.notify("profile_updated", user)
                
                class EmailObserver(Observer):
                    def __init__(self, email_service: EmailService):
                        self.email_service = email_service
                    
                    def update(self, event_type: str, data: Any) -> None:
                        if event_type == "profile_updated":
                            self.email_service.send_profile_update_email(data)
                
                # Setup
                user_service = UserService()
                user_service.attach(EmailObserver(email_service))
                user_service.attach(AuditObserver(audit_service))
                user_service.attach(AnalyticsObserver(analytics_service))
            """).strip(),
            explanation="Use Observer pattern when multiple objects need to be notified of changes",
            steps=[
                "1. Create Observer interface with update method",
                "2. Create Subject base class with attach/detach/notify methods",
                "3. Convert notification source to inherit from Subject",
                "4. Convert each notification target to implement Observer",
                "5. Replace manual notifications with notify calls"
            ],
            considerations=[
                "Use when you have one-to-many relationships",
                "Observers should handle their own errors",
                "Consider async notifications for performance",
                "Implement proper cleanup to prevent memory leaks"
            ],
            testing_notes="Test observer registration/removal, test notification with multiple observers"
        )
    ],
    
    "singleton": [
        RefactoringTemplate(
            pattern_name="singleton",
            scenario="Convert global configuration to thread-safe Singleton",
            before_code=dedent("""
                # Global variables - not thread-safe, hard to test
                DATABASE_HOST = "localhost"
                DATABASE_PORT = 5432
                DATABASE_NAME = "myapp"
                DEBUG_MODE = False
                
                def get_database_config():
                    return {
                        "host": DATABASE_HOST,
                        "port": DATABASE_PORT,
                        "name": DATABASE_NAME
                    }
                
                def set_debug_mode(enabled: bool):
                    global DEBUG_MODE
                    DEBUG_MODE = enabled
            """).strip(),
            after_code=dedent("""
                import threading
                from typing import Dict, Any
                
                class ConfigManager:
                    _instance = None
                    _lock = threading.Lock()
                    
                    def __new__(cls):
                        if cls._instance is None:
                            with cls._lock:
                                if cls._instance is None:
                                    cls._instance = super().__new__(cls)
                        return cls._instance
                    
                    def __init__(self):
                        if not hasattr(self, '_initialized'):
                            self._config = {
                                "database_host": "localhost",
                                "database_port": 5432,
                                "database_name": "myapp",
                                "debug_mode": False
                            }
                            self._config_lock = threading.Lock()
                            self._initialized = True
                    
                    def get(self, key: str, default: Any = None) -> Any:
                        with self._config_lock:
                            return self._config.get(key, default)
                    
                    def set(self, key: str, value: Any) -> None:
                        with self._config_lock:
                            self._config[key] = value
                    
                    def get_database_config(self) -> Dict[str, Any]:
                        with self._config_lock:
                            return {
                                "host": self._config["database_host"],
                                "port": self._config["database_port"],
                                "name": self._config["database_name"]
                            }
                
                # Usage
                config = ConfigManager()
                db_config = config.get_database_config()
                config.set("debug_mode", True)
            """).strip(),
            explanation="Use Singleton for configuration that needs global access and thread safety",
            steps=[
                "1. Create class with private _instance variable",
                "2. Implement thread-safe __new__ with double-check locking",
                "3. Add initialization guard in __init__",
                "4. Protect shared data with additional locks if needed",
                "5. Replace global variables with singleton methods"
            ],
            considerations=[
                "Only use for truly global resources (config, logging, connections)",
                "Ensure thread safety with proper locking",
                "Consider dependency injection for better testing",
                "Document singleton lifecycle and usage"
            ],
            testing_notes="Test thread safety, test singleton property, consider reset mechanism for tests"
        )
    ],
    
    "builder": [
        RefactoringTemplate(
            pattern_name="builder",
            scenario="Replace complex constructor with Builder pattern",
            before_code=dedent("""
                class DatabaseConnection:
                    def __init__(self, host: str, port: int, database: str, 
                                username: str, password: str, ssl_enabled: bool = False,
                                connection_timeout: int = 30, read_timeout: int = 60,
                                max_retries: int = 3, pool_size: int = 10,
                                charset: str = 'utf8', autocommit: bool = False):
                        self.host = host
                        self.port = port
                        self.database = database
                        self.username = username
                        self.password = password
                        self.ssl_enabled = ssl_enabled
                        self.connection_timeout = connection_timeout
                        self.read_timeout = read_timeout
                        self.max_retries = max_retries
                        self.pool_size = pool_size
                        self.charset = charset
                        self.autocommit = autocommit
                        
                        # Complex validation and setup logic...
                
                # Usage - hard to read and error-prone
                db = DatabaseConnection("localhost", 5432, "mydb", "user", "pass", 
                                      True, 45, 90, 5, 20, "utf8mb4", False)
            """).strip(),
            after_code=dedent("""
                class DatabaseConnection:
                    def __init__(self, host: str, port: int, database: str, 
                                username: str, password: str):
                        # Required parameters only
                        self.host = host
                        self.port = port
                        self.database = database
                        self.username = username
                        self.password = password
                        
                        # Optional parameters with defaults
                        self.ssl_enabled = False
                        self.connection_timeout = 30
                        self.read_timeout = 60
                        self.max_retries = 3
                        self.pool_size = 10
                        self.charset = 'utf8'
                        self.autocommit = False
                
                class DatabaseConnectionBuilder:
                    def __init__(self):
                        self._connection = None
                    
                    def with_host(self, host: str, port: int = 5432) -> 'DatabaseConnectionBuilder':
                        self._host = host
                        self._port = port
                        return self
                    
                    def with_database(self, name: str) -> 'DatabaseConnectionBuilder':
                        self._database = name
                        return self
                    
                    def with_credentials(self, username: str, password: str) -> 'DatabaseConnectionBuilder':
                        self._username = username
                        self._password = password
                        return self
                    
                    def with_ssl(self, enabled: bool = True) -> 'DatabaseConnectionBuilder':
                        self._ssl_enabled = enabled
                        return self
                    
                    def with_timeouts(self, connection: int = 30, read: int = 60) -> 'DatabaseConnectionBuilder':
                        self._connection_timeout = connection
                        self._read_timeout = read
                        return self
                    
                    def with_pool(self, size: int = 10) -> 'DatabaseConnectionBuilder':
                        self._pool_size = size
                        return self
                    
                    def build(self) -> DatabaseConnection:
                        # Validation
                        if not all(hasattr(self, attr) for attr in 
                                  ['_host', '_database', '_username', '_password']):
                            raise ValueError("Missing required connection parameters")
                        
                        # Create and configure connection
                        connection = DatabaseConnection(
                            self._host, self._port, self._database,
                            self._username, self._password
                        )
                        
                        # Set optional parameters
                        if hasattr(self, '_ssl_enabled'):
                            connection.ssl_enabled = self._ssl_enabled
                        if hasattr(self, '_connection_timeout'):
                            connection.connection_timeout = self._connection_timeout
                        if hasattr(self, '_read_timeout'):
                            connection.read_timeout = self._read_timeout
                        if hasattr(self, '_pool_size'):
                            connection.pool_size = self._pool_size
                        
                        return connection
                
                # Usage - much more readable
                db = (DatabaseConnectionBuilder()
                      .with_host("localhost", 5432)
                      .with_database("mydb")
                      .with_credentials("user", "pass")
                      .with_ssl(True)
                      .with_timeouts(connection=45, read=90)
                      .with_pool(20)
                      .build())
            """).strip(),
            explanation="Use Builder pattern for objects with many optional parameters (5+)",
            steps=[
                "1. Identify required vs optional parameters",
                "2. Create builder class with fluent interface methods",
                "3. Add validation in build() method",
                "4. Make builder methods return self for chaining",
                "5. Replace complex constructors with builder usage"
            ],
            considerations=[
                "Use for constructors with 5+ parameters or complex validation",
                "Builder provides better readability than long parameter lists",
                "Consider immutable objects with builders",
                "Add validation at appropriate construction steps"
            ],
            testing_notes="Test required parameter validation, test various optional parameter combinations"
        )
    ],
    
    "command": [
        RefactoringTemplate(
            pattern_name="command",
            scenario="Add undo/redo functionality using Command pattern",
            before_code=dedent("""
                class TextEditor:
                    def __init__(self):
                        self.content = ""
                    
                    def insert_text(self, position: int, text: str):
                        self.content = self.content[:position] + text + self.content[position:]
                    
                    def delete_text(self, position: int, length: int):
                        self.content = self.content[:position] + self.content[position + length:]
                    
                    def replace_text(self, position: int, length: int, text: str):
                        self.delete_text(position, length)
                        self.insert_text(position, text)
                    
                    # No undo/redo functionality - operations are irreversible
            """).strip(),
            after_code=dedent("""
                from abc import ABC, abstractmethod
                from typing import List
                
                class Command(ABC):
                    @abstractmethod
                    def execute(self) -> None:
                        pass
                    
                    @abstractmethod
                    def undo(self) -> None:
                        pass
                
                class TextEditor:
                    def __init__(self):
                        self.content = ""
                        self.history: List[Command] = []
                        self.current_position = -1
                    
                    def execute_command(self, command: Command) -> None:
                        # Remove any commands after current position (for new branch)
                        self.history = self.history[:self.current_position + 1]
                        
                        # Execute and add to history
                        command.execute()
                        self.history.append(command)
                        self.current_position += 1
                    
                    def undo(self) -> bool:
                        if self.current_position >= 0:
                            command = self.history[self.current_position]
                            command.undo()
                            self.current_position -= 1
                            return True
                        return False
                    
                    def redo(self) -> bool:
                        if self.current_position < len(self.history) - 1:
                            self.current_position += 1
                            command = self.history[self.current_position]
                            command.execute()
                            return True
                        return False
                
                class InsertTextCommand(Command):
                    def __init__(self, editor: TextEditor, position: int, text: str):
                        self.editor = editor
                        self.position = position
                        self.text = text
                    
                    def execute(self) -> None:
                        self.editor.content = (self.editor.content[:self.position] + 
                                             self.text + 
                                             self.editor.content[self.position:])
                    
                    def undo(self) -> None:
                        length = len(self.text)
                        self.editor.content = (self.editor.content[:self.position] + 
                                             self.editor.content[self.position + length:])
                
                class DeleteTextCommand(Command):
                    def __init__(self, editor: TextEditor, position: int, length: int):
                        self.editor = editor
                        self.position = position
                        self.length = length
                        self.deleted_text = ""
                    
                    def execute(self) -> None:
                        self.deleted_text = self.editor.content[self.position:self.position + self.length]
                        self.editor.content = (self.editor.content[:self.position] + 
                                             self.editor.content[self.position + self.length:])
                    
                    def undo(self) -> None:
                        self.editor.content = (self.editor.content[:self.position] + 
                                             self.deleted_text + 
                                             self.editor.content[self.position:])
                
                # Usage
                editor = TextEditor()
                editor.execute_command(InsertTextCommand(editor, 0, "Hello "))
                editor.execute_command(InsertTextCommand(editor, 6, "World!"))
                editor.undo()  # Removes "World!"
                editor.redo()  # Adds "World!" back
            """).strip(),
            explanation="Use Command pattern when you need undo/redo or operation queuing",
            steps=[
                "1. Create Command interface with execute() and undo() methods",
                "2. Create command classes for each operation type",
                "3. Add command history management to main class",
                "4. Implement undo/redo logic with position tracking",
                "5. Replace direct operations with command execution"
            ],
            considerations=[
                "Use when undo/redo, macro recording, or queuing is needed",
                "Commands should store enough state for reversal",
                "Consider memory usage for large command histories",
                "Commands can be serialized for persistence"
            ],
            testing_notes="Test execute/undo for each command type, test redo after undo, test history management"
        )
    ]
}


def get_refactoring_template(pattern_name: str, scenario: Optional[str] = None) -> Optional[RefactoringTemplate]:
    """Get a refactoring template for a specific pattern and scenario"""
    templates = REFACTORING_TEMPLATES.get(pattern_name.lower(), [])
    
    if not templates:
        return None
    
    if scenario:
        # Find template matching scenario
        for template in templates:
            if scenario.lower() in template.scenario.lower():
                return template
    
    # Return first template if no specific scenario or no match
    return templates[0]


def get_all_templates_for_pattern(pattern_name: str) -> List[RefactoringTemplate]:
    """Get all refactoring templates for a specific pattern"""
    return REFACTORING_TEMPLATES.get(pattern_name.lower(), [])


def list_available_patterns() -> List[str]:
    """List all patterns that have refactoring templates"""
    return list(REFACTORING_TEMPLATES.keys())


def generate_refactoring_guide(pattern_name: str) -> str:
    """Generate a comprehensive refactoring guide for a pattern"""
    templates = get_all_templates_for_pattern(pattern_name)
    
    if not templates:
        return f"No refactoring templates available for {pattern_name} pattern."
    
    guide = f"# {pattern_name.title()} Pattern Refactoring Guide\n\n"
    
    for i, template in enumerate(templates, 1):
        guide += f"## Scenario {i}: {template.scenario}\n\n"
        guide += f"**When to Apply**: {template.explanation}\n\n"
        
        guide += "### Before (Anti-Pattern/Problematic Code)\n"
        guide += "```python\n"
        guide += template.before_code
        guide += "\n```\n\n"
        
        guide += "### After (Pattern Implementation)\n"
        guide += "```python\n"
        guide += template.after_code
        guide += "\n```\n\n"
        
        guide += "### Refactoring Steps\n"
        for step in template.steps:
            guide += f"- {step}\n"
        guide += "\n"
        
        guide += "### Important Considerations\n"
        for consideration in template.considerations:
            guide += f"- {consideration}\n"
        guide += "\n"
        
        guide += f"### Testing Strategy\n"
        guide += f"{template.testing_notes}\n\n"
        
        guide += "---\n\n"
    
    return guide