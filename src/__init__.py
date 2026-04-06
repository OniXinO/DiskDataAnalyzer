"""
DiskDataAnalyzer - Універсальний аналізатор дисків для Windows

Основний пакет проєкту
"""

__version__ = '0.6.0'
__author__ = 'Created with Claude Code CLI'
__license__ = 'MIT'

from .core.analyze_disk import (
    analyze_disk,
    analyze_all_drives,
    get_disk_usage,
    format_bytes
)

__all__ = [
    'analyze_disk',
    'analyze_all_drives',
    'get_disk_usage',
    'format_bytes'
]
