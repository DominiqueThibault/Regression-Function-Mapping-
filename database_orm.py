"""Management of database interactions using SQLAlchemy ORM."""
import pandas as pd

from sqlalchemy import create_engine, inspect, Float, String, text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

# Maps classes.
Base = declarative_base()

class TrainingMapping(Base):
    """Declarative table configuration for mapping training data to the ideal functions."""
    __tablename__ = 'training_mapping'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    train_function: Mapped[str] = mapped_column(String(30))
    ideal_function: Mapped[str] = mapped_column(String(30))
    least_squares_error: Mapped[float] = mapped_column(Float)
    max_deviation: Mapped[float] = mapped_column(Float)
    average_deviation: Mapped[float] = mapped_column(Float)

class TestAssignment(Base):
    """Declarative table configuration for test data."""
    __tablename__ = 'test_assignment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    x: Mapped[float] = mapped_column(Float, index=True)
    y_test: Mapped[float] = mapped_column(Float, nullable=True, index=True)
    deviation: Mapped[float] = mapped_column(Float, index=True)
    ideal_function: Mapped[str] = mapped_column(String(30), nullable=True)

class DatabaseORM:
    """A representation of an object-related mapping database."""
    def __init__(self, db_url="sqlite:///functions.db"):
        """Establishing connectivity to database."""
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.inspector = inspect(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        print(self.inspector.get_table_names())

    def get_session(self):
        """Starts a session."""
        return self.session

    def load_csv_to_db(self, train_df, test_df, ideal_df):
        """Loads csv files to sqlite database"""
        filenames = [train_df, test_df, ideal_df]

        try:
            # Reads pd.DataFrames into sqlite database.
            train_df.to_sql("train", self.engine, if_exists="replace", index=False)
            test_df.to_sql("test", self.engine, if_exists="replace", index=False)
            ideal_df.to_sql("ideal", self.engine, if_exists="replace", index=False)

            #with self.engine.connect() as conn:
                #for _, row in test_df.iterrows():
                    #conn.execute(test_table.insert().values(**row.to_dict()))

        # Raises exception, if files are not in repository.
        except FileNotFoundError:
            for filename in filenames:
                print(f"Error: File '{filename}' not found.")
                raise
        else:
            print(f"Successfully loaded {len(filenames)} files.")

    def save_training_mapping(self, best_fit, training_mapping=None):
        """
        Saves mapping of training data to database.
        Returns:
            Four column data frame containing the four training functions, their
            corresponding ideal function, the least squares error, and the
            maximum deviation between the y values of both functions.
        """
        self.session.query(TrainingMapping).delete()
        self.session.commit()

        for train_func, info in best_fit.items():
            record = TrainingMapping(
                train_function=train_func,
                ideal_function=info["ideal_function"],
                least_squares_error=info["error"],
                max_deviation=info["max_dev"],
                average_deviation=info["avg_dev"]
            )
            self.session.add(record)

        self.session.commit()

    def save_test_assignments(self, assignments):
        """
        Saves test assignment to database.
        Returns:
            Four column data frame containing the test data points, their
            corresponding ideal function and the deviation between
            the y values.
        """
        self.session.query(TestAssignment).delete()
        self.session.commit()

        for item in assignments:
            if item is None:
                continue

            if item.get('deviation') is None:
                continue

            record = TestAssignment(
                x=float(item['x']),
                y_test=float(item['y_test']),
                ideal_function=item['ideal_function'],
                deviation=item['deviation']
            )
            self.session.add(record)

        self.session.commit()

        # Gets a connection, converts the SQL table to pandas DataFrame and saves it as CSV file.
        conn = self.engine.connect()

        training_mapping_df = pd.read_sql("SELECT * FROM training_mapping", conn)
        training_mapping_df.to_csv("training_mapping.csv", index=None)

        test_assignment_df = pd.read_sql("SELECT * FROM test_assignment", conn)
        test_assignment_df.to_csv("test_assignment.csv", index=None)

    def close(self):
        """Closes database connection."""
        self.session.close()