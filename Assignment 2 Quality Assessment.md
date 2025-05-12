# Second intermediate assignment – Quality assessment

Now that you’ve chosen a dataset, you must assess the quality and possibly perform data
cleaning. When determining the quality of a dataset, you could ask yourself many questions. We
have compiled a list of common questions below, but depending on the dataset you have
chosen, other questions may be applicable.

## Quality Assessment Questions

To help you assess the quality of your data set, we have compiled a list of questions to help you
get going. Don't view this as an exhaustive list where you must answer each question in your
report, but as questions that data engineers could ask to assess the quality of data sets.

Questions:

- Are there any NULL values, and if so, how many? Are they correctly encoded as NULL, or
    is there a placeholder (0 or 999)?
- Are all columns usable, or just a few?
- Does the dataset contain outliers? How can you detect them, and can they be
    corrected?
- If the data contains units, for example, for temperature, is it Celsius or Fahrenheit? Do
    the values make sense for that unit?
- How are values encoded? For instance, which date formats (and time zones) are used?
    Are values properly normalized?
- If the data contains text, what is the encoding? For example, UTF8 or ASCII.
- Are the values plausible, and do they make sense? For example, if the data contains
    addresses or phone numbers, do they resemble actual, real-life locations and phone
    numbers?
- When using multiple data sources, can you find clear keys to join the data? Are these
    keys represented in the same way in both datasets? For example, one dataset could
    represent a US state as CA, while the other denotes California.
- Do all files have the same number of columns? Do the types match? Is there a clear
    schema? Are there duplicate fields in the records?
- Are the types correct for the values they represent? A classic example is a table column
    with only integer values but with a string type.
- Do the digits in the file have separators? Are there separators for the decimals and for
    every 1000? For example, is 1 million written as 1,000,000.0 or as 1.000.000,0? Are the
    separators consistent?
- If the data has to be parsed, is it easy to parse? For example, does the CSV have
    consistent separators and quoted strings? Or, in the case of HTML, is the HTML incorrect
    or incomplete?


## Data Cleaning

Now that you've assessed the quality of your data set, how do you plan to clean it? Which tools
will you use? Do you need to perform any transformations or normalizations to make sense of
the data or to prepare it for your intended use case?

As mentioned in the previous assignment, you are expected to use SQL where possible. Of
course, other tools may be necessary to perform all cleaning and transformation.
Some example tools to process data are:

- Python
- JSON/XML readers
- Unix Command Line Tools
- Deequ
- OpenRefine

## Rubric

The final report consists of all (polished) assignments merged into one coherent and concise
report. Initially, however, your weekly assignments will be graded on a pass/fail basis only. The
report for this assignment will become part of the final report and be graded based on how well
you assessed the quality of the data and how well you cleaned it.

Quality Assessment:

1. Only minimal quality checks were performed, and very little explanation was given.
2. The quality was assessed reasonably well, but some existing issues were not identified.
    A decent explanation was given.
3. Data quality was assessed exhaustively and creatively, i.e., all relevant parts of the data
    set were inspected meaningfully, and the quality issues that were found were explained
    in detail.

Data Cleaning:

1. Quality issues were resolved poorly. Questionable decisions were made that were not
    justified well.
2. Quality issues were resolved reasonably well. The tools used are OK but maybe not the
    most efficient. Some decisions were justified, and some were not.
3. All quality observed issues were resolved using appropriate tools. Decisions made
    during this process were justified well.

Depending on your project, we recognize that this week's assignment (Quality Assessment) will
overlap to some extent with next week's assessment (Wrangling and Reshaping), as some data
sets must be reshaped to some extent before all quality issues can be resolved. If you think this
is the case for your project, and you are not able to address all quality issues in this week's
report, please explain why and how you plan to address the issues that you observed in the next
assignment.


## Report

This week's report should include last week's report, i.e., you will incrementally build the final
report by adding each week's assignment. Please add the most important code snippets and
SQL queries you used for this assignment. Note that you must move these code snippets to the
appendix for the final report. You can link to your GitHub repository in your report, but we will
grade you on what we see in the report, so please add the most important code snippets.

## Questions From Last Year

**Should my data cleaning pipeline be re-usable?** Yes. Data engineering is not a one-time thing,
as data sets are always updated. Your data cleaning pipeline should apply to new data that is
added.

**Can I use a private data set?** Using a private (i.e., non-public) data set makes it very difficult for
us to grade your work, so we prefer that you do not.


