"""Common utility functions for tool schema definitions

This file contains common functions and utilities used in all tool schema definition files.
"""

from typing import Dict, Any, Optional
from vita.config import DEFAULT_LANGUAGE

# Global tool description registry
TOOL_DESCRIPTIONS_REGISTRY: Dict[str, Dict[str, Any]] = {}

# Global language configuration
_current_language = DEFAULT_LANGUAGE

# Global schema manager registry
_schema_managers: Dict[str, 'ToolSchemaManager'] = {}

def get_global_language() -> str:
    """Get current global language configuration

    Returns:
        Current language setting
    """
    return _current_language

def register_tool_descriptions(domain: str, descriptions: Dict[str, Dict[str, Any]]):
    """Register tool descriptions for a specific domain
    
    Args:
        domain: Domain name (e.g., 'delivery', 'instore', 'ota', 'toolkit')
        descriptions: Mapping dictionary from tool names to descriptions
    """
    TOOL_DESCRIPTIONS_REGISTRY[domain] = descriptions

def get_tool_description(domain: str, tool_name: str) -> Optional[Dict[str, Any]]:
    """Get tool description from registry
    
    Args:
        domain: Domain name
        tool_name: Tool name
        
    Returns:
        Tool description dictionary, returns None if not found
    """
    domain_descriptions = TOOL_DESCRIPTIONS_REGISTRY.get(domain, {})
    return domain_descriptions.get(tool_name)

def generate_tool_docstring(domain: str, tool_name: str, language: str = None) -> str:
    """Generate complete docstring for tool by combining all information

    Args:
        domain: Domain name
        tool_name: Tool name
        language: Language setting, if None then use global language setting

    Returns:
        Complete formatted docstring
    """
    if language is None:
        language = get_global_language()

    # If schema manager exists, prioritize using manager descriptions
    if domain in _schema_managers:
        manager = _schema_managers[domain]
        # Temporarily set language
        original_language = manager.language_config
        manager.set_language(language)
        tool_desc = manager.get_tool_description(tool_name)
        # Restore original language
        manager.set_language(original_language)
    else:
        tool_desc = get_tool_description(domain, tool_name)

    if not tool_desc:
        return ""
    
    # Build docstring
    docstring_parts = []
    
    # Description
    docstring_parts.append(tool_desc['description'])
    
    # Preconditions
    docstring_parts.append("Preconditions:")
    docstring_parts.append(f"    - {tool_desc['preconditions']}")
    
    # Postconditions
    docstring_parts.append("Postconditions:")
    docstring_parts.append(f"    - {tool_desc['postconditions']}")
    
    # Arguments
    docstring_parts.append("")
    docstring_parts.append("Args:")
    for arg_name, arg_desc in tool_desc['args'].items():
        docstring_parts.append(f"    {arg_name}: {arg_desc}")
    
    # Return value
    docstring_parts.append("")
    docstring_parts.append("Returns:")
    docstring_parts.append(f"    {tool_desc['returns']}")
    
    return "\n".join(docstring_parts)

def get_domain_from_class(cls) -> Optional[str]:
    """Extract domain name from class name or module path

    Args:
        cls: Class object

    Returns:
        Domain name, returns None if cannot determine
    """
    # Try to extract domain from class name
    class_name = cls.__name__.lower()

    # Common domain patterns
    if 'delivery' in class_name:
        return 'delivery'
    elif 'instore' in class_name:
        return 'instore'
    elif 'ota' in class_name:
        return 'ota'
    elif 'toolkitbase' in class_name or 'generictoolkit' in class_name:
        return 'toolkit'

    # Try to extract from module path
    module_name = cls.__module__.lower()
    if 'delivery' in module_name:
        return 'delivery'
    elif 'instore' in module_name:
        return 'instore'
    elif 'ota' in module_name:
        return 'ota'
    elif 'toolkit' in module_name:
        return 'toolkit'

    return None


def set_global_language(language: str):
    """Set global language configuration

    Args:
        language: Language setting ('chinese' or 'english')
    """
    global _current_language
    _current_language = language

    # Update language configuration for all registered schema managers
    for manager in _schema_managers.values():
        manager.set_language(language)

    # Re-register all tool descriptions
    for domain, manager in _schema_managers.items():
        TOOL_DESCRIPTIONS_REGISTRY[domain] = manager.get_tool_descriptions()


# Common tool description management class
class ToolSchemaManager:
    """Tool schema manager, provides common tool description management functionality"""
    
    def __init__(self, domain: str, **language_descriptions: Dict[str, Any]):
        """Initialize tool schema manager
        
        Args:
            domain: Domain name
            **language_descriptions: Language-keyed tool descriptions, 
                e.g. chinese=TOOL_DESCRIPTIONS_ZH, english=TOOL_DESCRIPTIONS_EN.
                Each value is a Dict[str, Dict[str, Any]] mapping tool names to descriptions.
        """
        self.domain = domain
        self.descriptions = dict(language_descriptions)
        
        # Backward compatibility: also store the original ZH/EN references
        self.descriptions_zh = self.descriptions.get("chinese", {})
        self.descriptions_en = self.descriptions.get("english", {})
        
        self.language_config = get_global_language()
        
        self._update_tool_type_mapping()

        _schema_managers[domain] = self
        self._register_with_global_registry()

    def set_language(self, language: str):
        """Set language configuration

        Args:
            language: Language setting ('chinese' or 'english')
        """
        self.language_config = language
        self._update_tool_type_mapping()

    def _update_tool_type_mapping(self):
        """Update tool type mapping"""
        lang = self.language_config
        type_labels = {
            "chinese":  {"GENERIC": "通用工具", "READ": "读取工具", "WRITE": "写入工具"},
            "english":  {"GENERIC": "Generic Tool", "READ": "Read Tool", "WRITE": "Write Tool"},
            "japanese": {"GENERIC": "汎用ツール", "READ": "読み取りツール", "WRITE": "書き込みツール"},
            "french":   {"GENERIC": "Outil générique", "READ": "Outil de lecture", "WRITE": "Outil d'écriture"},
            "russian":  {"GENERIC": "Универсальный инструмент", "READ": "Инструмент чтения", "WRITE": "Инструмент записи"},
            "arabic":   {"GENERIC": "أداة عامة", "READ": "أداة قراءة", "WRITE": "أداة كتابة"},
            "hindi":    {"GENERIC": "सामान्य उपकरण", "READ": "पठन उपकरण", "WRITE": "लेखन उपकरण"},
            "thai":     {"GENERIC": "เครื่องมือทั่วไป", "READ": "เครื่องมืออ่าน", "WRITE": "เครื่องมือเขียน"},
            "spanish":  {"GENERIC": "Herramienta genérica", "READ": "Herramienta de lectura", "WRITE": "Herramienta de escritura"},
            "korean":      {"GENERIC": "일반 도구", "READ": "읽기 도구", "WRITE": "쓰기 도구"},
            "indonesian":  {"GENERIC": "Alat Umum", "READ": "Alat Baca", "WRITE": "Alat Tulis"},
            "hebrew":      {"GENERIC": "כלי כללי", "READ": "כלי קריאה", "WRITE": "כלי כתיבה"},
            "turkish":     {"GENERIC": "Genel Araç", "READ": "Okuma Aracı", "WRITE": "Yazma Aracı"},
            "vietnamese":  {"GENERIC": "Công cụ chung", "READ": "Công cụ đọc", "WRITE": "Công cụ ghi"},
            "malay":       {"GENERIC": "Alat Am", "READ": "Alat Baca", "WRITE": "Alat Tulis"},
            "belarusian":  {"GENERIC": "Агульны інструмент", "READ": "Інструмент чытання", "WRITE": "Інструмент запісу"},
            "punjabi":     {"GENERIC": "ਆਮ ਔਜ਼ਾਰ", "READ": "ਪੜ੍ਹਨ ਔਜ਼ਾਰ", "WRITE": "ਲਿਖਣ ਔਜ਼ਾਰ"},
            "kazakh":      {"GENERIC": "Жалпы құрал", "READ": "Оқу құралы", "WRITE": "Жазу құралы"},
            "khmer":       {"GENERIC": "ឧបករណ៍ទូទៅ", "READ": "ឧបករណ៍អាន", "WRITE": "ឧបករណ៍សរសេរ"},
            "burmese":     {"GENERIC": "အထွေထွေကိရိယာ", "READ": "ဖတ်ရန်ကိရိယာ", "WRITE": "ရေးရန်ကိရိယာ"},
            "lao":         {"GENERIC": "ເຄື່ອງມືທົ່ວໄປ", "READ": "ເຄື່ອງມືອ່ານ", "WRITE": "ເຄື່ອງມືຂຽນ"},
            "tamil":       {"GENERIC": "பொது கருவி", "READ": "படிக்கும் கருவி", "WRITE": "எழுதும் கருவி"},
            "telugu":      {"GENERIC": "సాధారణ సాధనం", "READ": "చదవడం సాధనం", "WRITE": "వ్రాయడం సాధనం"},
        }
        self.tool_type_mapping = type_labels.get(lang, type_labels["english"])
    
    def get_tool_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """Get tool descriptions based on language configuration"""
        if self.language_config in self.descriptions:
            return self.descriptions[self.language_config]
        elif "english" in self.descriptions:
            return self.descriptions["english"]
        elif "chinese" in self.descriptions:
            return self.descriptions["chinese"]
        else:
            return next(iter(self.descriptions.values()), {})
    
    def get_tool_description(self, tool_name: str) -> Dict[str, Any]:
        """Get description of specific tool by name
        
        Args:
            tool_name: Tool name
            
        Returns:
            Dictionary containing tool description, preconditions, postconditions, arguments, return value and tool type
        """
        return self.get_tool_descriptions().get(tool_name, {})
    
    def get_all_tool_names(self) -> list:
        """Get list of all available tool names

        Returns:
            List of tool names
        """
        return list(self.get_tool_descriptions().keys())

    def get_tools_by_type(self, tool_type: str) -> Dict[str, Dict[str, Any]]:
        """Get all tools of specific type

        Args:
            tool_type: Tool type (GENERIC, READ, or WRITE)

        Returns:
            Mapping dictionary from tool names to descriptions
        """
        return {
            name: desc for name, desc in self.get_tool_descriptions().items()
            if desc["tool_type"] == tool_type
        }

    def get_tool_count_by_type(self) -> Dict[str, int]:
        """Get tool count by type

        Returns:
            Mapping dictionary from tool type to count
        """
        counts = {}
        for desc in self.get_tool_descriptions().values():
            tool_type = desc["tool_type"]
            counts[tool_type] = counts.get(tool_type, 0) + 1
        return counts

    def get_tool_args(self, tool_name: str) -> Dict[str, str]:
        """Get arguments of specific tool by name

        Args:
            tool_name: Tool name

        Returns:
            Mapping dictionary from argument names to descriptions
        """
        tool_desc = self.get_tool_descriptions().get(tool_name, {})
        return tool_desc.get("args", {})

    def get_tool_returns(self, tool_name: str) -> str:
        """Get return value description of specific tool by name

        Args:
            tool_name: Tool name

        Returns:
            String describing tool return content
        """
        tool_desc = self.get_tool_descriptions().get(tool_name, {})
        return tool_desc.get("returns", "")

    def _register_with_global_registry(self):
        """Register tool descriptions to global toolkit registry"""
        try:
            register_tool_descriptions(self.domain, self.get_tool_descriptions())
        except ImportError:
            # If toolkit_schema is not available, skip registration
            pass

# Convenience function for creating and managing tool schemas
def create_tool_schema_manager(domain: str, descriptions_zh: Optional[Dict[str, Dict[str, Any]]] = None,
                              descriptions_en: Optional[Dict[str, Dict[str, Any]]] = None,
                              **extra_languages: Dict[str, Dict[str, Any]]) -> ToolSchemaManager:
    """Convenience function to create tool schema manager
    
    Args:
        domain: Domain name
        descriptions_zh: Chinese tool descriptions (backward compatible positional arg)
        descriptions_en: English tool descriptions (backward compatible positional arg)
        **extra_languages: Additional language descriptions as keyword args
            e.g. japanese=TOOL_DESCRIPTIONS_JA
        
    Returns:
        Tool schema manager instance
    """
    language_descriptions = {}
    if descriptions_zh is not None:
        language_descriptions["chinese"] = descriptions_zh
    if descriptions_en is not None:
        language_descriptions["english"] = descriptions_en
    language_descriptions.update(extra_languages)
    return ToolSchemaManager(domain, **language_descriptions)

# Common tool type mapping
def get_tool_type_mapping(language: str = None) -> Dict[str, str]:
    """Get tool type mapping
    
    Args:
        language: Language setting, if None then use global language setting

    Returns:
        Mapping from tool type to localized name
    """
    if language is None:
        language = get_global_language()

    type_labels = {
        "chinese":  {"GENERIC": "通用工具", "READ": "读取工具", "WRITE": "写入工具"},
        "english":  {"GENERIC": "Generic Tool", "READ": "Read Tool", "WRITE": "Write Tool"},
        "japanese": {"GENERIC": "汎用ツール", "READ": "読み取りツール", "WRITE": "書き込みツール"},
        "french":   {"GENERIC": "Outil générique", "READ": "Outil de lecture", "WRITE": "Outil d'écriture"},
        "russian":  {"GENERIC": "Универсальный инструмент", "READ": "Инструмент чтения", "WRITE": "Инструмент записи"},
        "arabic":   {"GENERIC": "أداة عامة", "READ": "أداة قراءة", "WRITE": "أداة كتابة"},
        "hindi":    {"GENERIC": "सामान्य उपकरण", "READ": "पठन उपकरण", "WRITE": "लेखन उपकरण"},
        "thai":     {"GENERIC": "เครื่องมือทั่วไป", "READ": "เครื่องมืออ่าน", "WRITE": "เครื่องมือเขียน"},
        "spanish":  {"GENERIC": "Herramienta genérica", "READ": "Herramienta de lectura", "WRITE": "Herramienta de escritura"},
        "korean":      {"GENERIC": "일반 도구", "READ": "읽기 도구", "WRITE": "쓰기 도구"},
        "indonesian":  {"GENERIC": "Alat Umum", "READ": "Alat Baca", "WRITE": "Alat Tulis"},
        "hebrew":      {"GENERIC": "כלי כללי", "READ": "כלי קריאה", "WRITE": "כלי כתיבה"},
        "turkish":     {"GENERIC": "Genel Araç", "READ": "Okuma Aracı", "WRITE": "Yazma Aracı"},
        "vietnamese":  {"GENERIC": "Công cụ chung", "READ": "Công cụ đọc", "WRITE": "Công cụ ghi"},
        "malay":       {"GENERIC": "Alat Am", "READ": "Alat Baca", "WRITE": "Alat Tulis"},
        "belarusian":  {"GENERIC": "Агульны інструмент", "READ": "Інструмент чытання", "WRITE": "Інструмент запісу"},
        "punjabi":     {"GENERIC": "ਆਮ ਔਜ਼ਾਰ", "READ": "ਪੜ੍ਹਨ ਔਜ਼ਾਰ", "WRITE": "ਲਿਖਣ ਔਜ਼ਾਰ"},
        "kazakh":      {"GENERIC": "Жалпы құрал", "READ": "Оқу құралы", "WRITE": "Жазу құралы"},
        "khmer":       {"GENERIC": "ឧបករណ៍ទូទៅ", "READ": "ឧបករណ៍អាន", "WRITE": "ឧបករណ៍សរសេរ"},
        "burmese":     {"GENERIC": "အထွေထွေကိရိယာ", "READ": "ဖတ်ရန်ကိရိယာ", "WRITE": "ရေးရန်ကိရိယာ"},
        "lao":         {"GENERIC": "ເຄື່ອງມືທົ່ວໄປ", "READ": "ເຄື່ອງມືອ່ານ", "WRITE": "ເຄື່ອງມືຂຽນ"},
        "tamil":       {"GENERIC": "பொது கருவி", "READ": "படிக்கும் கருவி", "WRITE": "எழுதும் கருவி"},
        "telugu":      {"GENERIC": "సాధారణ సాధనం", "READ": "చదవడం సాధనం", "WRITE": "వ్రాయడం సాధనం"},
    }
    return type_labels.get(language, type_labels["english"])