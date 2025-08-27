"""Data loading and processing module."""

import pandas as pd
import glob
from typing import List, Optional
from config import DataConfig


class DataLoader:
    """Handles loading and preprocessing of data files."""
    
    def __init__(self, config: DataConfig):
        self.config = config
        self.data_folder = config.data_folder
        self.required_columns = config.required_columns
    
    def load_files(self) -> Optional[pd.DataFrame]:
        """Load all Excel/CSV files from the data folder."""
        data_files = glob.glob(f'{self.data_folder}/*.xlsx') + glob.glob(f'{self.data_folder}/*.csv')
        
        if not data_files:
            print(f"WARNING: No data files found in {self.data_folder}/ folder")
            return None
        
        all_data = []
        for file_path in data_files:
            df = self._load_single_file(file_path)
            if df is not None:
                all_data.append(df)
        
        return self._combine_data(all_data) if all_data else None
    
    def _load_single_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """Load and validate a single file."""
        try:
            df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                print(f"WARNING: {file_path} missing columns: {missing_columns}")
                return None
            
            # Clean data
            for col in self.required_columns:
                df[col] = df[col].astype(str).str.strip()
            
            print(f"✓ Loaded {len(df)} records from {file_path}")
            return df
            
        except Exception as e:
            print(f"ERROR loading {file_path}: {str(e)}")
            return None
    
    def _combine_data(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """Combine dataframes and remove duplicates."""
        combined_df = pd.concat(dataframes, ignore_index=True)
        
        initial_count = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['Tool', 'Action'], keep='first')
        final_count = len(combined_df)
        
        if initial_count != final_count:
            print(f"Removed {initial_count - final_count} duplicate entries")
        
        # Create searchable text
        combined_df['searchable_text'] = (
            combined_df['Tool'].astype(str) + ' ' + 
            combined_df['Action'].astype(str) + ' ' + 
            combined_df['Summary'].astype(str)
        )
        
        return combined_df