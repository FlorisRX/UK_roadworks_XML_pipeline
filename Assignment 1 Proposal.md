# First assignment – Proposal

The first assignment is to pick a _raw and unprocessed data set_ and write a project proposal describing how
you will use this data set to create a _data product_. You'll create something that's much easier and more
efficient to use than an initial _unwieldy_ data set.

The task of the data engineer is not to load an already preprocessed dataset into Python and train a neural
network on it, for example. The data engineer does all the work that comes before that: Quality
Assessment, Reshaping/Wrangling, etc. So, make sure to search for a dataset that is not yet fully
preprocessed to make the project interesting and challenging from a data engineering perspective.

## **Sources**

Pick a dataset from one of the following sources:

- Awesome Data: https://github.com/awesomedata/awesome-public-datasets
- Hugging Face: https://huggingface.co/datasets

You can also find a dataset anywhere on the Internet! Government websites often have public, raw, and
unprocessed datasets.

You may have used data sets from these sources in previous courses:

- Kaggle: https://www.kaggle.com/datasets
- UCI: https://archive.ics.uci.edu/datasets

The data sets on these websites are often processed to the point where they are already a finished data
product, which is not what you're looking for. You can pick a data set from these sources, but please keep
this in mind so that you don't pick a data set that has already been fully processed.

## **Requirements**

The data set must be _tabular_ , consisting of _records with attributes_ and fit in a table_._ You cannot pick image,
video, _or_ audio data sets.

The data set _cannot be small_. As a rule of thumb, pick a data set that contains at least 1 million records. This
is not a hard requirement, but the data set cannot be too small. please justify why you picked your data set
if it is smaller than 1 million records.

The data set should not be an already fully processed data product. Good examples of raw and unprocessed
data are JSON/XML files from the web. These records can't immediately be put into a structured table
without processing.

**IMPORTANT NOTE:** Many of you have plenty of experience with Pandas in Python, but you will be expected
to use SQL where possible during the project. You must have a good reason for not using SQL for a
processing step. For example, if the database system that you are using does not support reading your XML
dataset, you can use whatever tool you like to convert the XML to something that your chosen database
system can read, like CSV/Parquet/JSON.

This will be explained in more detail in the next assignment, but if you're curious, some of the database
systems that you can use for SQL are DuckDB, SQLite, PostgreSQL, and ClickHouse (and many more!).

## **Report**

When looking at data sets, write down the ones that caught your eye but that you _did not pick_ (at least 2
and at most 5). Briefly describe why you found the data set interesting and what the final data product
would have been. Also, describe why you did not end up picking this data set.


For the data set you pick, describe in more detail why you found this data set interesting, how you plan on
processing it, and what the final data product will be. Explain why you picked this data set over the data sets
that you did not pick.

You may change the dataset any time during the course, but your final report must contain all assignments
and be about one dataset.

**Data Set Questions**

To help you inspect and choose a data set, we have compiled a list of questions to help you get going. Don't
view this as an exhaustive list where you must answer each question in your report, but more as questions
that data engineers may want to know before committing to a project. This can help you judge whether the
data set that you find interesting is suitable.

Questions:

- What dataset did you pick?
- What is the data model of the dataset (e.g. relational/graph/unstructured)?
- What is the storage format (e.g. JSON, CSV, RDF, raw text, Parquet, etc.)?
- What is the size of the dataset (e.g. 5GB)?
- Does the dataset come from one source or multiple sources? What are the sources? (e.g. weather
    institute temperature data from different countries, JSON logs from web applications)
- How frequently (if ever) does the dataset need to be updated to stay relevant?
- Without going too in-depth, what can you already say about the data? For example, how many
    columns/rows does it have? Has it been preprocessed by someone else before, or is it “raw data”?
- Why did you pick this dataset? What do you intend to use it for?
    - Feature extraction and preprocessing for a machine learning application (i.e. “getting the
       dataset ready for the data scientists”)
    - Powering a dashboard or visualization (i.e. “getting the dataset ready for the data analyst”)

## Rubric

The final report consists of all (polished) assignments merged into one coherent and concise report. Initially,
however, your weekly assignments will be graded on a pass/fail basis only. This project proposal will
become part of the final report and be graded based on how ambitious your project is and how well
thought out your plan for it is.

Ambitious:

1. The chosen data set is already in decent shape (e.g., a single CSV file without many flaws) and is
    already close to the proposed final data product; therefore, processing will not be very challenging.
2. The chosen data set will require somewhat challenging processing to achieve the proposed final
    data product.
3. The chosen data set is not in great shape (e.g., JSON/XML files with inconsistent attributes in the
    records) and is quite far from the proposed final data product (e.g., needs to be enriched with data
    from other sources); therefore, processing it will be challenging.

Plan:


1. The plan for the final data product is not well thought out or described.
2. The plan is well-thought-out and described but fairly straightforward.
3. The plan is novel, interesting, well-thought-out, and described.

## Previous Projects

Here are some projects from last year to give you some inspiration:

1. Creating a PyTorch data loader (e.g., to be used for weather predictions) from public data from
    public KNMI (Dutch Royal Weather Institute) data.
2. Converting very nasty XML data about artworks from the Rijksmuseum so that it can easily be
    analyzed using SQL.
3. Preparing Wikipedia data dumps so that they can be used for graph query processing.

All three projects were done last year, and all three converted unwieldy data sets into final data products
that could be used easily and efficiently.

All three projects were done last year, and all three converted unwieldy data sets into final data products
that could be used easily and efficiently

## Questions From Last Year

**What is a data product?** The data product you have to create is more than just a CSV/Parquet file. Most
data sets are not "static" and must be continuously updated. The data product is the entire "data processing
pipeline", i.e., how you got from the unwieldy input data set to the final, easy-to-access data, e.g., files
hosted in the cloud or a REST API. So, it also is not an ML model or data dashboard in a web browser.

**How "dirty" does the data set I pick need to be?** There is no strict requirement here, as it all depends on
the intended goal. You can pick a clean data set but still have ambitious data engineering plans with it, e.g.,
by enriching it with other data.

**Can the data set I pick contain multiple storage formats?** Yes, that's not a problem. Combining multiple
storage formats into a coherent data product can be very interesting and challenging.

**Does the final data product need to be a single table/file?** No, depending on your project, it could make
sense to have multiple tables in a schema.