from typing import TypeAlias
from hat.tdspy.mermaid_flow_chart_2_json import Decision, Process, BaseElement, Terminator


Element: TypeAlias = Decision | Process | BaseElement | Terminator