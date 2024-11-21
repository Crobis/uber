import subprocess
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand


class Command(CollectStaticCommand):
    def handle(self, *args, **options):
        # Step 1: Run the default collectstatic process
        print('Running collectstatic 2')
        super().handle(*args, **options)

        # # Step 2: Run Tailwind CSS build process
        # try:
        #     print("Running Tailwind CSS build...")
        #     subprocess.run(
        #         ["npm", "run", "build:css"],
        #         cwd=self.get_project_root(),
        #         check=True,
        #     )
        #     print("Tailwind CSS build completed successfully!")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error occurred while building Tailwind CSS: {e}")
        #     raise

    def get_project_root(self):
        """
        Return the project root directory.
        Modify this method if your project root isn't the same as the location of manage.py.
        """
        import os
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
