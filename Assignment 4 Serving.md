# Fourth intermediate report – Serving

After the wrangling and reshaping phase, your dataset should now be ready for distribution. In the lecture, different aspects of serving data were discussed. It is now up to you to decide how your dataset can be served best. You don’t actually have to host the data or deploy your API somewhere, it is enough to describe how you would serve it. Explain your decisions, and argue why your serving solution matches the dataset and the intended use case.

While deciding which serving approach to take, keep the following questions in mind. Note they may not be exhaustive – they are only intended to help you get started. Try to formulate your assignment as part of your final report, don’t enumerate a list of answers to the example questions.

## **Serving Questions**

- How should end-users access your processed dataset? Would it make sense to, for example, store the data in a database, and build an API to query/access parts of the dataset? If so, what type of API should you use (e.g. REST, SQL, GraphQL)? Or should they always download the entire dataset? Why?
- Which format does your final data product use? Is this the most convenient format for users? For example, if you have a dataset in Parquet format, should users always get the entire Parquet file? Or is it better for users to query the dataset and get back results in another format, e.g., JSON? Why?
- On what infrastructure will you be hosting the data or API? E.g. a “machine under your desk”, in the cloud (S3 for files or cloud computing for APIs), using a CDN, etc. Why?
- Would partitioning improve the efficiency of accessing/using your dataset? For example, if your dataset contains weather data from the entire world, would it make sense to partition the dataset by country so that users can access specific parts of the data without downloading the entire dataset? Why?
- Does your dataset contain any sensitive data? Or do you only want certain people to access certain parts? What type of access control would you use?
- Are there any costs associated with the way in which you want to serve the data? If so, who do you want to pay for it? Is there a pricing scheme attached to data access, or are the costs manageable for the organisation serving the data?
- What kind of load do you expect on your served data? How can you handle this load (or larger loads)?
- Try to think ahead of the lifecycle of your data product. Will your chosen serving setup work well if people need automated/continuous or repeated access to the data?
- If these questions do not apply well to your specific use case, please explain to us in detail how your dataset should be served, and why.

## **Rubric**

The final report consists of all (polished) assignments merged into one coherent and concise report. Initially, however, your weekly assignments will be graded on a pass/fail basis only. The report for this assignment will become part of the final report and be graded based on how well you identified the right transformation steps and tools, and how well you performed and automated these steps.

Data access:

1. Data access is not well thought out. Serving the final data product is not much more convenient than e-mailing an unwieldy CSV file around, and it cannot easily be automated. Different access patterns are not considered.
2. The chosen serving setup matches the use case, but data access is still inefficient in some cases. For instance, users might want or need specific slices of the data, which cannot be accessed conveniently or efficiently.
3. Data access is thought out in detail. The access patterns for the use case are considered, and with the proposed approach, the data will be served efficiently and conveniently for the users to download the parts they need. Access can easily be automated in data pipelines.

Meta-aspects (e.g. pricing, handling high loads, access control/security/privacy):

1. The report only describes how the data could be served or distributed, without thinking of meta-aspects at all.
2. Some meta-aspects were named, but not all of them were properly resolved. Some important meta-aspects might be missing. Some solutions may not be suitable for the chosen method of serving, or the intended use case.
3. A wide range of meta-aspects is discussed. For each meta-aspect, a well-thought-out solution is proposed, or it is explained in depth why this will not be an issue.

Actually serving (bonus points):

1. While not required, if you put effort into actually serving your data, e.g., uploading your processed data to HuggingFace, or experimenting with hosting a REST API locally, we will be impressed!

## **Report**

This week's report should include last week's report, i.e., you will incrementally build the final report by adding each week's assignment. Please add the most important code snippets and SQL queries you used for this assignment. Note that you must move these code snippets to the appendix for the final report. You can link to your GitHub repository in your report, but we will grade you on what we see in the report, so please add the most important code snippets.

## **Lessons From Last Year**

Please think about your project specifically, instead of making broad statements about serving strategies in general. What makes your plan for serving appropriate for your project? Think about how your data will be used specifically, make decisions, and justify them.