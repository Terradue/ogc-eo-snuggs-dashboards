#import streamlit as st
from multiapp import MultiApp
from apps import (
    s_expression,
)

apps = MultiApp()

apps.add_app("S expressions", s_expression.app)

apps.run()
