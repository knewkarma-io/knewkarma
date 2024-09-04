import os.path
from typing import Literal, Union

import pandas as pd

try:
    import matplotlib.pyplot as plt

    visualisation_deps_installed: bool = True
except ImportError:
    visualisation_deps_installed = False

try:
    import torch
    from transformers import (
        DistilBertTokenizer,
        DistilBertForSequenceClassification,
        PreTrainedModel,
    )

    ml_deps_installed: bool = True
except ImportError:
    ml_deps_installed = False

from .tools.general import console, OUTPUT_PARENT_DIR
from .tools.console import Notify

__all__: list = [
    "ANALYSIS_TO_MODEL_MAP",
    "DISTRIBUTION_LABELS_AND_COLOURS",
    "plot_bar_chart",
    "get_model",
    "analyse_text",
    "analyse_texts",
    "plot_analysis",
    "visualisation_deps_installed",
    "ml_deps_installed",
]

notify = Notify

ANALYSIS_TO_MODEL_MAP: dict = {
    "sentiment": "sentiment_analysis",
    "emotion": "emotion_detection",
}

# Define labels and colours in a dictionary
DISTRIBUTION_LABELS_AND_COLOURS: dict[str, dict[str, list[str]]] = {
    "sentiment": {
        "labels": ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"],
        "colours": ["red", "#FF9999", "skyblue", "green", "#99FF99"],
    },
    "emotion": {
        "labels": ["anger", "fear", "joy", "love", "sadness", "surprise"],
        "colours": ["#FF6347", "#FFD700", "#32CD32", "#FF69B4", "#1E90FF", "#FFA500"],
    },
}

if visualisation_deps_installed:

    def plot_bar_chart(
        data: dict[str, int],
        title: str,
        xlabel: str,
        ylabel: str,
        colours: list[str],
        filename: str,
        figure_size: tuple[int, int] = (10, 5),
    ):
        """
        Plots a bar chart for the given data.

        :param data: A dictionary where keys are the categories and values are the counts or frequencies.
        :type data: list[str, int]
        :param title: The title of the plot.
        :type title: str
        :param xlabel: The label for the x-axis.
        :type xlabel: str
        :param ylabel: The label for the y-axis.
        :type ylabel: str
        :param colours: A list of colours to use for the bars in the chart.
        :type colours: list[str]
        :param filename: The name of the file where the plot will be saved.
        :type filename: str
        :param figure_size: The size of the figure (width, height). Defaults to (10, 5).
        :type figure_size: tuple[int, int]
        """
        plt.figure(figsize=figure_size)
        plt.bar(list(data.keys()), list(data.values()), color=colours)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(f"{filename}.png")
        console.print(f"{title} saved to [link file://{filename}.png]{filename}.png")

else:

    def plot_bar_chart(*args, **kwargs):
        console.print(
            "The function 'plot_bar_chart' requires visualisation dependencies "
            "Please install them by running 'pip install knewkarma[visualization]'."
        )


if ml_deps_installed and visualisation_deps_installed:

    def get_model(
        model_type: Literal["sentiment_analysis", "emotion_detection"],
        mode: Literal["load", "download"],
        status: console.status = None,
    ) -> tuple[DistilBertTokenizer, PreTrainedModel]:
        """
        Downloads or loads the appropriate model and tokenizer for the given analysis type.

        This function will download the respective model locally if it doesn't already exist
        or if the mode is set to "download". Otherwise, it gets loaded from local storage.

        :param model_type: The type of model to use for the analysis. Either 'sentiment_analysis' or 'emotion_detection'.
        :type model_type: Literal[str]
        :param mode: The mode to either 'load' the model if it exists or 'download' it forcefully.
        :type mode: Literal[str]
        :return: A tuple containing the tokenizer and the pre-trained model.
        :rtype: tuple[DistilBertTokenizer, PreTrainedModel]
        """
        if model_type == "sentiment_analysis":
            model_path = "distilbert_base_uncased_sst2_english"
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        elif model_type == "emotion_detection":
            model_path = "distilbert_base_uncased_emotion"
            model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
        else:
            raise ValueError(
                "Invalid model_type. Choose either 'sentiment_analysis' or 'emotion_detection'."
            )

        # Define the absolute path for the model
        absolute_model_path: str = os.path.join(OUTPUT_PARENT_DIR, model_path)

        # Check if the model exists locally and load it if in 'load' mode
        if os.path.exists(absolute_model_path) and mode == "load":
            tokenizer: DistilBertTokenizer = DistilBertTokenizer.from_pretrained(
                absolute_model_path
            )
            model: PreTrainedModel = (
                DistilBertForSequenceClassification.from_pretrained(absolute_model_path)
            )
        else:
            # Download the model and save it locally
            if status:
                status.update(
                    f"Downloading pre-trained model '{model_name}' for {model_type.replace('_', ' ')}..."
                )
            tokenizer: DistilBertTokenizer = DistilBertTokenizer.from_pretrained(
                model_name
            )
            model: PreTrainedModel = (
                DistilBertForSequenceClassification.from_pretrained(model_name)
            )
            tokenizer.save_pretrained(absolute_model_path)
            model.save_pretrained(absolute_model_path)
            notify.ok(
                f"Pre-trained model '{model_name}' downloaded to [link file://{absolute_model_path}]{absolute_model_path}"
            )

        return tokenizer, model

    def analyse_text(
        text: str,
        analysis_type: Literal["sentiment", "emotion"],
    ) -> Union[int, float, bool]:
        """
        Analyzes the sentiment or emotion of a single text.

        :param text: The input text to be analysed.
        :param analysis_type: The type of analysis to perform. Either 'sentiment' or 'emotion'.
        :return: The predicted class as an integer, float, or boolean.
        """

        tokenizer, model = get_model(
            model_type=ANALYSIS_TO_MODEL_MAP[analysis_type], mode="load"
        )

        # Tokenize the input text and make predictions
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            clean_up_tokenization_spaces=True,
        )
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        predicted_class: Union[int, float, bool] = torch.argmax(probs, dim=1).item()

        return predicted_class

    def analyse_texts(
        texts_list: list[str],
        analysis_type: Literal["sentiment", "emotion"],
    ) -> tuple[list[str], list[str]]:
        """
        Analyzes the sentiment or emotion of multiple texts.

        :param texts_list: A list of texts to be analysed.
        :param analysis_type: The type of analysis to perform. Either 'sentiment' or 'emotion'.
        :return: A tuple containing the original texts and their corresponding predicted labels.
        """
        labels: list = DISTRIBUTION_LABELS_AND_COLOURS[analysis_type]["labels"]
        analysis_results: list = []

        for text in texts_list:
            label_index = analyse_text(analysis_type=analysis_type, text=text)
            analysis_results.append(labels[label_index])

        return texts_list, analysis_results

    def plot_analysis(
        posts: list[str],
        labels: list[str],
        analysis_type: Literal["sentiment", "emotion"],
        filename: str,
    ):
        """
        Plots the distribution of sentiments or emotions for a list of posts.

        :param posts: A list of posts to be analysed.
        :param labels: A list of labels corresponding to the analysed posts.
        :param analysis_type: The type of analysis to perform. Either 'sentiment' or 'emotion'.
        :param filename: The name of the file where the plot will be saved.
        """
        expected_labels: list = DISTRIBUTION_LABELS_AND_COLOURS[analysis_type]["labels"]
        colours: list = DISTRIBUTION_LABELS_AND_COLOURS[analysis_type]["colours"]

        # Convert posts and labels to DataFrame
        dataframe: pd.DataFrame = pd.DataFrame(
            {"Post": posts, analysis_type.capitalize(): labels}
        )

        # Count the occurrences of each category and reindex to include all expected labels
        distribution_counts = (
            dataframe[analysis_type.capitalize()]
            .value_counts()
            .reindex(expected_labels, fill_value=0)
        )

        plot_bar_chart(
            data=distribution_counts.to_dict(),
            title=f"{analysis_type.capitalize()} Distribution",
            xlabel=analysis_type.capitalize(),
            ylabel="Count",
            colours=colours,
            filename=filename,
        )

else:
    message: str = (
        f"Analysis and visualisation dependencies are required in order to use this feature. "
        f"Please install them by running 'pip install knewkarma[analysis]' and 'pip install knewkarma[visualisation]"
    )

    def get_model(*args, **kwargs):
        console.print(message)

    def analyse_text(*args, **kwargs):
        console.print(message)

    def analyse_texts(*args, **kwargs):
        console.print(message)

    def plot_analysis(*args, **kwargs):
        console.print(message)
