from lamini.experiment.base_generator import BaseGenerator
from lamini.generation.base_prompt_object import PromptObject
from copy import deepcopy

import sqlite3


class QuestionsToConceptsGenerator(BaseGenerator):
    """
    Takes a list of questions and returns a list of concepts that are relevant to the questions.
    """

    def __init__(
        self,
        model,
        client=None,
        name=None,
        role=None,
        instruction=None,
        output_type=None,
        **kwargs,
    ):

        name = name or "QuestionsToConceptsGenerator"
        role = (
            role
            or "You are a helpful assistant that takes a list of common questions and returns a list of concepts that are relevant to the concepts."
        )
        instruction = (
            instruction
            or """Given the list of questions, return short concepts that are relevant to the questions, separated by commas. Do not include any other information in your response.
        Questions:
        {questions}

        Concepts:"""
        )

        output_type = output_type or {
            "concepts_list": "str"
        }  # This is the intermediate output type

        super().__init__(
            client=client,
            model=model,
            name=name,
            role=role,
            instruction=instruction,
            output_type=output_type,
            **kwargs,
        )

    def postprocess(self, result):
        # Turn the string result, formatted as {"concepts_list": "concept1, concept2, concept3"}, into a list of concept objects
        concepts_list_object = result.response["concepts_list"]

        concepts_list_object = concepts_list_object.replace(
            "[", ""
        )  # remove square brackets
        concepts_list_object = concepts_list_object.replace("]", "")

        concepts_list = concepts_list_object.split(",")  # split into list of concepts

        concepts_list = [
            concept.strip() for concept in concepts_list
        ]  # remove whitespace
        concepts_list = [
            concept for concept in concepts_list if concept
        ]  # remove empty strings

        # Create a list of concept PromptObjects, each with a concept field
        concepts = []
        for concept in concepts_list:
            # Deep copy the history stored in result prompt object to avoid shared references
            new_prompt_obj = PromptObject(
                prompt=deepcopy(result.prompt),
                data=deepcopy(result.data),
                response=deepcopy(result.response),
            )
            new_prompt_obj.data["concept"] = concept
            concepts.append(new_prompt_obj)

        return concepts


class QuestionToConceptGenerator(BaseGenerator):
    """
    Takes a single question and returns a single concept that is relevant to the question.
    """

    def __init__(
        self,
        model,
        client=None,
        name=None,
        role=None,
        instruction=None,
        output_type=None,
        **kwargs,
    ):
        name = name or "QuestionToConceptGenerator"
        role = (
            role
            or "You are a helpful assistant that takes a single question and returns a single concept that is relevant to the question."
        )
        instruction = (
            instruction
            or """Given the question, return a single concept that is relevant to the question.
        Question:
        {question}

        Concept:"""
        )

        output_type = output_type or {"concept": "str"}

        super().__init__(
            client=client,
            model=model,
            name=name,
            role=role,
            instruction=instruction,
            output_type=output_type,
            **kwargs,
        )


class ConceptToSQLInterpretationGenerator(BaseGenerator):
    """
    Takes a concept and returns the SQL interpretation of the concept.
    """

    def __init__(
        self,
        model,
        client=None,
        name=None,
        role=None,
        instruction=None,
        output_type=None,
        **kwargs,
    ):
        name = name or "ConceptToSQLInterpretationGenerator"
        role = (
            role
            or "You are a helpful assistant that takes a concept and returns the SQL interpretation of the concept, which is just the calculation of the concept in a SQL fragment."
        )
        instruction = (
            instruction
            or """Given the concept, return the SQL interpretation of the concept, which is just the calculation of the concept in a SQL fragment.
        Concept:
        {concept}

        SQL Interpretation:"""
        )

        output_type = output_type or {"sql": "str"}

        super().__init__(
            client=client,
            model=model,
            name=name,
            role=role,
            instruction=instruction,
            output_type=output_type,
            **kwargs,
        )


class BaseSQLGenerator(BaseGenerator):
    """Base class for SQL-related generators with common database functionality."""

    SUPPORTED_DB_TYPES = {
        "sqlite": lambda params: sqlite3.connect(
            params["database"] if isinstance(params, dict) else params
        )
    }
    metadata_keys = ["schema"]  # required before super init

    def __init__(
        self,
        model,
        client=None,
        schema=None,
        db_type=None,
        db_params=None,
        name=None,
        role=None,
        instruction=None,
        output_type=None,
        **kwargs,
    ):
        # Initialize conn before calling super().__init__ to ensure it exists
        self.conn = None

        super().__init__(
            client=client,
            model=model,
            name=name or "BaseSQLGenerator",
            role=role or "You are a SQL expert.",
            instruction=instruction or "Base SQL Generator",
            output_type=output_type,  # set by subclasses
            **kwargs,
        )

        # Initialize database connection if params provided
        if db_type and db_params:
            self._initialize_db(db_type, db_params)
            self.schema = self._get_schema_from_db() if not schema else schema

            # Add db_type and db_params to input, instead of schema
            self.input["db_type"] = db_type
            self.input["db_params"] = db_params
            self.input.pop("schema", None)
        elif schema:
            self.schema = schema
        else:
            raise ValueError(
                "Must provide schema string, or db_type and db_params to connect to a database and extract the schema"
            )

    @classmethod
    def add_db_support(cls, db_type, connection_factory):
        """Add support for a new database type."""
        cls.SUPPORTED_DB_TYPES[db_type] = connection_factory

    def _initialize_db(self, db_type, db_params):
        """Initialize database connection."""
        if db_type not in self.SUPPORTED_DB_TYPES:
            raise ValueError(
                f"Unsupported database type: {db_type}. "
                f"Supported types are: {list(self.SUPPORTED_DB_TYPES.keys())}"
            )

        try:
            connection_factory = self.SUPPORTED_DB_TYPES[db_type]
            self.conn = connection_factory(db_params)
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def _get_schema_from_db(self):
        """Extract schema information from connected database."""
        if not self.conn:
            raise RuntimeError("No database connection available")

        cur = self.conn.cursor()
        schema_string = ""

        # Get list of tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        for table in tables:
            table_name = table[0]
            schema_string += f"Schema for table '{table_name}':\n"

            # Get table schema
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()

            # Get sample row
            cur.execute(f"SELECT * FROM {table_name} LIMIT 1;")
            sample_row = cur.fetchone()
            sample_row = list(sample_row) if sample_row is not None else []

            # Format column information
            for index, column in enumerate(columns):
                column_name = column[1]
                column_type = column[2]
                sample_value = sample_row[index] if index < len(sample_row) else None
                schema_string += f"Column: {column_name} | Type: {column_type} | Sample Value: {sample_value}\n"

            schema_string += "\n"

        return schema_string

    def execute_query(self, query):
        """Execute a SQL query if database connection is available."""
        if not self.conn:
            raise RuntimeError(
                "No database connection available. Initialize with db_type and db_params to execute queries."
            )

        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def __del__(self):
        """Cleanup database connection if it exists."""
        if self.conn:
            self.conn.close()


class SchemaToSQLGenerator(BaseSQLGenerator):
    def __init__(
        self,
        model,
        client=None,
        schema=None,
        db_type=None,
        db_params=None,
        schema_definitions=None,
        terms_in_questions=None,
        output_type=None,
        instruction=None,
        name="SchemaToSQLGenerator",
        role="You are a SQL expert with 15 years of experience writing complex SQL queries.",
        execute_sql=False,
    ):
        instruction = (
            instruction
            or """Consider the following database schema:
        {schema}"""
        )

        if schema_definitions:
            instruction += """
            Here are the definitions of terms used in the schema:
            {schema_definitions}
            """

        if terms_in_questions:
            instruction += """
            Here is a glossary of terms used in the questions:
            {terms_in_questions}
            """

        instruction += """
        Write a sqlite query to answer the following question: {question}
        
        Now, let's think step by step:
        1. Analyze the Question: Understand what information is being requested
        2. Map to Database Schema: Identify relevant tables and columns
        3. Construct SQL Query: Write an optimized query that answers the question
        4. Validate: Ensure the query is correct and efficient
        """

        output_type = output_type or {
            "schema_to_sql_thinking_steps": "str",
            "sql_query": "str",
        }

        super().__init__(
            client=client,
            model=model,
            schema=schema,
            db_type=db_type,
            db_params=db_params,
            name=name,
            role=role,
            instruction=instruction,
            output_type=output_type,
        )

        self.schema = schema
        self.schema_definitions = schema_definitions
        self.terms_in_questions = terms_in_questions

        self.execute_sql = execute_sql

    def __call__(self, prompt_obj, debug=False):
        # Add schema and optional components to prompt
        prompt_obj.data["schema"] = self.schema
        if self.schema_definitions:
            prompt_obj.data["schema_definitions"] = self.schema_definitions
        if self.terms_in_questions:
            prompt_obj.data["terms_in_questions"] = self.terms_in_questions
        result = super().__call__(prompt_obj, debug)

        if self.execute_sql:
            if hasattr(self, "conn"):
                query = result.response["sql_query"]
                try:
                    result.response["sql_execution"] = self.execute_query(query)
                    result.data["execution_status"] = "success"
                except Exception as e:
                    result.data["execution_status"] = "failed"

                    # For SQLDebugger, if it's the next generator in pipeline
                    result.data["error_sql"] = query
                    result.data["error_message"] = str(e)
            else:
                self.logger.warning(
                    "No database connection available. Cannot execute SQL query. Initialize with db_type and db_params to execute queries."
                )

        return result


class SQLDebuggerGenerator(BaseSQLGenerator):
    def __init__(
        self,
        model,
        output_type=None,
        instruction=None,
        client=None,
        schema=None,
        db_type=None,
        db_params=None,
    ):

        instruction = (
            instruction
            or """SQL Query Debugger:
        You are provided with a user's SQL query and the following error message:
        Error: {error_message}

        Database Schema:
        {schema}

        Fix any issues in the SQL query using the provided schema. Apply these rules:
        1. String Comparisons: Use LOWER() for case-insensitive matches unless exact match needed
        2. Aliasing: Ensure calculated fields have appropriate aliases
        3. GROUP BY: Include all non-aggregated columns
        4. Calculations: Use parentheses to clarify order of operations
        5. WHERE Clauses: Verify conditions match column types
        6. Date Functions: Use appropriate date formatting
        7. CASE Statements: Handle all possible cases
        8. Performance: Avoid redundant operations

        The query to fix is:
        {error_sql}

        Think step by step. Then, provide the corrected SQL query.
        """
        )

        output_type = output_type or {
            "sql_debugger_thinking_steps": "str",
            "corrected_sql": "str",
        }

        super().__init__(
            client=client,
            model=model,
            schema=schema,
            db_type=db_type,
            db_params=db_params,
            name="SQLDebugger",
            role="You are a SQL debugging expert with 30 years of experience.",
            instruction=instruction,
            output_type=output_type,
        )

    def __call__(self, prompt_obj, debug=False):
        prompt_obj.data["schema"] = self.schema
        return super().__call__(prompt_obj, debug)


# SchemaConceptToQuestionGenerator


# def main():
#     response = ConceptToSQLInterpretationGenerator(
#         role="You are a helpful assistant that takes a concept and returns the SQL interpretation of the concept. You are given a sample question where the query calculation is included (in addition to potential other distracting info). You should return the SQL interpretation of the concept, which is just the calculation of the concept in a SQL fragment.",
#         concepts=[
#             {
#                 "concept": "Share of Market (SOM) analysis",
#                 "description": "Share of market (can be units, volume, or value share)",
#                 "sample_question": "Which manufacturer had the highest SOM in Q2 2024?",
#                 "sample_query_calculation": "SELECT manufacturer FROM colgate WHERE strftime('%Y-%m', month_445) IN ('2024-04', '2024-05', '2024-06') GROUP BY manufacturer ORDER BY SUM(sales_value) DESC LIMIT 1;",
#             },
#             {
#                 "concept": "YTD",
#                 "description": "Year to date",
#                 "sample_question": "How is Colgate's unit SOM performance YTD?",
#                 "sample_query_calculation": """SELECT
#     SUM(CASE WHEN ""manufacturer"" = 'COLGATE' THEN ""sales_units"" ELSE 0 END) AS total_units_colgate,
#     SUM(""sales_units"") AS total_units_all,
#     (SUM(CASE WHEN ""manufacturer"" LIKE 'COLGATE' THEN ""sales_units"" ELSE 0 END) * 100.0) / SUM(""sales_units"") AS colgate_unit_share
# FROM
#     dev_athena_hub.cur_nielsen.us_toothpaste
# WHERE
#     ""year_value"" = EXTRACT(YEAR FROM CURRENT_DATE)
#     AND ""market_desc"" = 'Total US xAOC';""",
#             }
#         ],
#     ).run(debug=True)


#     response = ConceptAndSamplesToSQLInterpretationGenerator(
#         concepts=[
#             {
#                 "concept": "Share of Market (SOM) analysis",
#                 "description": "Share of market (can be units, volume, or value share)",
#                 "sample_question": "Which manufacturer had the highest SOM in Q2 2024?",
#                 "sample_query_calculation": "SELECT manufacturer FROM colgate WHERE strftime('%Y-%m', month_445) IN ('2024-04', '2024-05', '2024-06') GROUP BY manufacturer ORDER BY SUM(sales_value) DESC LIMIT 1;",
#                 "blahblahblah": "blahblahblah",
#             }
#         ]
#     ).run(debug=True)


# if __name__ == "__main__":
#     main()
