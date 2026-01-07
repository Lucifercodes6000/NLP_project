import graphviz
try:
    dot = graphviz.Digraph(comment='Test')
    dot.node('A', 'Test Node')
    dot.render('test_graphviz_output', view=False, format='png')
    print("Graphviz test successful: test_graphviz_output.png created")
except Exception as e:
    print(f"Graphviz test failed: {e}")
