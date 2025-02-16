import pandas as pd

# csv_to_quiz.py
def load_quiz_from_csv(file_path):
    try:
        # Load CSV with proper handling for quoted values
        df = pd.read_csv(file_path, quotechar='"')
        
        # Clean column names by stripping leading/trailing spaces
        df.columns = df.columns.str.strip()

        # Ensure required columns are present
        required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("The uploaded CSV is missing required columns.")

        # Replace 'none' with 'None of these'
        option_cols = ['option1', 'option2', 'option3', 'option4', 'correct_answer']
        for col in option_cols:
            df[col] = df[col].replace({'none': 'None of these', 'NONE': 'None of these'}, regex=True)

        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV: {str(e)}")