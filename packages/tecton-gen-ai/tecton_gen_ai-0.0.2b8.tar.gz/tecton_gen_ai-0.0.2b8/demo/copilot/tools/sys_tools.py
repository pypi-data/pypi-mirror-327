import matplotlib.pyplot as plt
import io
import base64
import json
from utils import _log, _log_image, _err, _success


def generate_graph(data: str, title: str, x_label: str, y_label: str, graph_type: str = "line") -> str:
    """
    Generate a graph using Matplotlib and return it as a base64-encoded image.

    Args:
        data: A JSON string containing the data for the graph. Example: '{"x": ["Jan", "Feb", "Mar"], "series": {"Series1": [10, 20, 30], "Series2": [15, 25, 35]}}'
        title: The title of the graph.
        x_label: The label for the x-axis.
        y_label: The label for the y-axis.
        graph_type: The type of graph to generate. Options: "line", "bar". Default is "line".

    Returns:
        str: Error message or success message
    """

    try:
        _log(":eye: Generating graph")

        data = json.loads(data)
        x = data.get("x", [])
        series = data.get("series", {})

        if not x or not series or not all(len(x) == len(y) for y in series.values()):
            raise ValueError("Invalid data: 'x' and all series must be non-empty and of the same length.")

        plt.figure(figsize=(8, 5))

        for label, y in series.items():
            if graph_type == "line":
                plt.plot(x, y, marker='o', linestyle='-', label=label)
            elif graph_type == "bar":
                plt.bar(x, y, label=label)
            else:
                raise ValueError("Invalid graph_type. Supported types: 'line', 'bar'.")

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.grid(True)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        _log_image(title, image_base64)

        return _success("Graph generated successfully")
    except Exception as e:
        return _err(f"{str(e)}")
