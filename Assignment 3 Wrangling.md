# Third intermediate report – Wrangling & Reshaping

Now that you have assessed the quality of your dataset, you have to decide how you want to wrangle
and reshape it. What to wrangle, and how, as well as the final shape of the dataset all depend on the
use-case that you have chosen. Again, we have compiled a list of questions that a data engineer might
ask themselves before they decide how to reshape the data and which tools to use.

## Reshaping Questions

- Imagine you are the end user of this dataset (e.g., a data scientist/analyst), what would be the
    easiest structure of the dataset to use in the intended downstream task?
- Is your dataset semi-structured (e.g., XML/JSON)? Do you want the resulting dataset to be
    structured (e.g., Parquet, CSV)? How do you plan to convert it?
- If your dataset comes from multiple sources, do you intend to combine them all into one
    dataset? How do you want to combine multiple (possibly different) schemas?
- Did you notice any issues or peculiarities with your dataset in the quality assessment stage,
    which you can solve by transforming the data somehow? For example, are all the dates in the
    same format? Are all the temperatures in the same unit (Celsius/Fahrenheit)?
- Can you process all of the data in bulk, or do you have to use a batch-based, streaming or
    distributed approach? Related to that, how well does your pipeline or workflow scale, if the
    input data were to grow bigger?
- Which tool or technology fits best with your required wrangling and reshaping steps?
- Can you automate the wrangling and reshaping stage, for instance to handle updates or
    simplify making small changes to the output data product?
- Would the dataset benefit from any (de-)normalization? For example, if your dataset contains a
    table with “orders”, containing an order ID and customer ID, and a table with “ordered_items”,
    which contains an order ID and an item ID, would it help to join “orders” and “ordered_items”
    so that it is easier to find which customer ordered which items? Or, vice-versa, is your dataset
    already pre-joined, and can you un-join it by creating two tables?

## Data Reshaping

After making a plan on how to reshape the data, we want you to actually perform this transformation.
This includes the cleaning steps identified in the Quality Assessment assignment, as well as the
wrangling/reshaping steps necessary to create your final dataset. Again, use SQL where possible and
make sure that the steps in your pipeline can be automated.

Some common tools that can be useful in the wrangling & reshaping stage are the following:

- SQL
- Python + Pandas/Polars/?
- Spark
- Airflow
- Dbt

## Rubric

The final report consists of all (polished) assignments merged into one coherent and concise report.
Initially, however, your weekly assignments will be graded on a pass/fail basis only. The report for this
assignment will become part of the final report and be graded based on how well you identified the
right transformation steps and tools, and how well you performed and automated these steps.

Correctness:


1. Mistakes were made in wrangling and/or transforming the data, introducing errors into the
    dataset and affecting the usability of the final product.
2. The transformations were performed correctly, but did not take pre-existing issues of the data
    into account, thus propagating errors into the output data product.
3. The transformations are performed correctly. Suitable transformations were identified, e.g.,
    appropriate (fuzzy) join keys were chosen, and the data was reshaped in a sensible manner.
    The final data is of high quality.

Use case:

1. The final data product does not support the intended use case; the end-user will need to
    perform additional pre-processing to get the data ready for their application.
2. The data product supports the intended use case better than the original data, but still requires
    some additional processing.
3. The final data product clearly supports the intended use case; the end-user (e.g., data
    analyst/scientist) can easily build their application on top.

Tooling/automation:

1. The pipeline is hacked together or the chosen tools are not very well-aligned, and the pipeline
    will definitely have to be modified to support future changes and other updates.
2. The pipeline consists of reasonable tools that did the job, but could be automated or
    implemented more effectively.
3. The appropriate tools were used to perform the wrangling & reshaping task. The pipeline can
    easily be automated to simplify deployment for future changes or other updates.

## **Report**

This week's report should include last week's report, i.e., you will incrementally build the final report by
adding each week's assignment. Please add the most important code snippets and SQL queries you
used for this assignment. Note that you must move these code snippets to the appendix for the final
report. You can link to your GitHub repository in your report, but we will grade you on what we see in
the report, so please add the most important code snippets.

IMPORTANT NOTE (again): Many of you have plenty of experience with Pandas in Python, but you will
be expected to use SQL where possible during the project. You must have a good reason for not using
SQL for a processing step. For example, if the database system that you are using does not support
reading your XML dataset, you can use whatever tool you like to convert the XML to something that
your chosen database system can read, like CSV/Parquet/JSON.

## **Question From Last Year**

_“I have quite some null values in my data set, and I am not sure what to replace them with.”_
Answer: Null values aren’t always bad! Sometimes null is the only way to represent missing values.
However, if you want to use the data for ML applications, you might need to change them or leave them
out. It really depends on the use case you have chosen, what you have to do with null values. The goal
of the quality assessment is to identify null values, and think about how they impact your use case,
and what you have to do about them (if anything - for many use cases it’s okay to leave them in).