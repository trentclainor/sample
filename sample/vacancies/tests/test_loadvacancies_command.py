import hashlib
from io import StringIO
from unittest.mock import mock_open, patch

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management import CommandError, call_command
from rest_framework.test import APITestCase

from sample.vacancies.management.commands.loadvacancies import Command as LoadVacanciesCommand
from sample.vacancies.models import Vacancy


class LoadVacanciesTestCase(APITestCase):
    providers = LoadVacanciesCommand.all_providers

    def test_wrong_command_should_return_error_message(self):
        try:
            call_command('loadvacancies', 'temp')
        except CommandError as e:
            self.assertIn("argument providers: invalid choice: 'temp'", str(e))

    def test_wrong_provider_parameter_should_return_error_message(self):
        try:
            call_command('loadvacancies', '-t')
        except CommandError as e:
            self.assertIn("unrecognized arguments: -t", str(e))

    @patch('os.path.exists', return_value=False)
    def test_import_provider_when_not_have_data_file_command_should_return_error_message(self, exists):
        stderr = StringIO()
        call_command('loadvacancies', 'pwc', stderr=stderr)
        stderr = stderr.getvalue().strip()
        self.assertIn("{}/pwc.xml not exist".format(settings.SCRAPERS_DATA_DIR), stderr)

    @patch('os.path.exists', return_value=False)
    def test_import_all_providers_when_not_have_data_command_should_return_error_message(self, exists):
        stderr = StringIO()
        call_command('loadvacancies', '-a', stderr=stderr)
        stderr = stderr.getvalue().strip()
        for provider in self.providers:
            file = "{}/{}.xml".format(settings.SCRAPERS_DATA_DIR, provider)
            exists.assert_any_call(file)
            self.assertIn("{} not exist".format(file), stderr)

    @patch('os.path.exists')
    @patch('shutil.move')
    @patch('os.remove')
    def test_import_provider_when_have_empty_data_file_command_should_return_how_much_import(self, *args):
        stdout = StringIO()
        with patch('sample.vacancies.management.commands.loadvacancies.open', mock_open(read_data='')):
            call_command('loadvacancies', 'pwc', stdout=stdout)
        self.assertIn("0 from 0", stdout.getvalue())

    @patch('os.path.exists')
    @patch('shutil.move')
    @patch('os.remove')
    @pytest.mark.django_db
    def test_import_provider_when_file_with_1_vacancy_and_command_should_return_how_much_import(self, *args):
        XML = """<?xml version="1.0" ?>
<root>
    <Jobs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <job>
            <Category>Government and public sector</Category>
            <StartingDate> </StartingDate>
            <Description>Due to increased demand from our clients...</Description>
            <CountryCode>GB</CountryCode>
            <Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/878384/Organisational-Change-Consultant/</Job_URL>
            <Country>United Kingdom</Country>
            <Experience>All our people need to demonstrate the skills and behaviours that support us in ...</Experience>
            <EndingDate> </EndingDate>
            <Customer_Job_Code>22344BR</Customer_Job_Code>
            <Location>Belfast</Location>
            <Type>Full Time</Type>
            <SalaryRange> </SalaryRange>
            <Job_Title>Organisational Change Consultant</Job_Title>
        </job>
    </Jobs>
</root>
"""
        stdout = StringIO()
        with patch('sample.vacancies.management.commands.loadvacancies.open', mock_open(read_data=XML)):
            call_command('loadvacancies', 'pwc', stdout=stdout)
        stdout = stdout.getvalue().strip()
        self.assertIn("1 from 1", stdout)
        vacancy_cnt = Vacancy.objects.count()
        self.assertIn('{} from 1'.format(vacancy_cnt), stdout)
        soup = BeautifulSoup(XML, "html.parser")
        for job in soup.findAll('job'):
            source_hash = hashlib.sha256(str(job).encode('utf-8')).hexdigest()
            vacancy = Vacancy.objects.get(source_hash=source_hash)
            assert vacancy.name == job.job_title.text.strip()

    @patch('os.path.exists')
    @patch('shutil.move')
    @patch('os.remove')
    @pytest.mark.django_db
    def test_import_provider_when_file_with_3_vacancy_and_2_is_unique_command_should_return_how_much_import(
        self, *args):
        XML = """<?xml version="1.0" ?>
<root>
	<Jobs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<job>
			<Category>Retail and Consumer</Category>
			<StartingDate> </StartingDate>
			<Description>PwC and Salesforce   PwC is the ... Learn more here  www.pwc.com/uk/diversity</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/870656/Manager-Salesforce-Solutions-Architect/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours ... and relationships.</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>18843BR</Customer_Job_Code>
			<Location>London</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
			<Job_Title>Manager - Salesforce Solutions Architect</Job_Title>
		</job>
		<job>
			<Category>Government and public sector</Category>
			<StartingDate> </StartingDate>
			<Description>Due to increased demand from our clients...</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/878384/Organisational-Change-Consultant/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours that support us in ...</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>22344BR</Customer_Job_Code>
			<Location>Belfast</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
			<Job_Title>Organisational Change Consultant</Job_Title>
		</job>
		<job>
			<Category>Retail and Consumer</Category>
			<StartingDate> </StartingDate>
			<Description>PwC and Salesforce   PwC is the ... Learn more here  www.pwc.com/uk/diversity</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/870656/Manager-Salesforce-Solutions-Architect/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours ... and relationships.</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>18843BR</Customer_Job_Code>
			<Location>London</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
			<Job_Title>Manager - Salesforce Solutions Architect</Job_Title>
		</job>
	</Jobs>
</root>
"""
        stdout = StringIO()
        with patch('sample.vacancies.management.commands.loadvacancies.open', mock_open(read_data=XML)):
            call_command('loadvacancies', 'pwc', stdout=stdout)
        stdout = stdout.getvalue().strip()
        self.assertIn("2 from 3", stdout)
        vacancy_cnt = Vacancy.objects.count()
        self.assertIn('{} from 3'.format(vacancy_cnt), stdout)
        soup = BeautifulSoup(XML, "html.parser")
        for job in soup.findAll('job'):
            source_hash = hashlib.sha256(str(job).encode('utf-8')).hexdigest()
            vacancy = Vacancy.objects.get(source_hash=source_hash)
            assert vacancy.name == job.job_title.text.strip()

    @patch('os.path.exists')
    @patch('shutil.move')
    @patch('os.remove')
    @pytest.mark.django_db
    def test_import_provider_when_file_with_1_corrupter_vacancy_and_command_should_return_how_much_import(self, *args):
        XML = """<?xml version="1.0" ?>
<root>
	<Jobs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<job>
			<Category>Government and public sector</Category>
			<StartingDate> </StartingDate>
			<Description>Due to increased demand from our clients...</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/878384/Organisational-Change-Consultant/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours that support us in ...</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>22344BR</Customer_Job_Code>
			<Location>Belfast</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
		</job>
	</Jobs>
</root>"""
        stdout = StringIO()
        stderr = StringIO()
        with patch('sample.vacancies.management.commands.loadvacancies.open', mock_open(read_data=XML)):
            call_command('loadvacancies', 'pwc', stdout=stdout, stderr=stderr)
        stdout = stdout.getvalue().strip()
        stderr = stderr.getvalue().strip()
        self.assertIn("0 from 1", stdout)
        vacancy_cnt = Vacancy.objects.count()
        self.assertIn('{} from 1'.format(vacancy_cnt), stdout)
        soup = BeautifulSoup(XML, "html.parser")
        self.assertIn(str(soup.findAll('job')[0]), stderr)

    @patch('os.path.exists')
    @patch('shutil.move')
    @patch('os.remove')
    @pytest.mark.django_db
    def test_when_file_with_1_corrupter_and_1_normal_vacancy_and_command_should_return_how_much_import_and_wrong_xml(self, *args):
        XML = """<?xml version="1.0" ?>
<root>
	<Jobs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
		<job>
			<Category>Government and public sector</Category>
			<StartingDate> </StartingDate>
			<Description>Due to increased demand from our clients...</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/878384/Organisational-Change-Consultant/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours that support us in ...</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>22344BR</Customer_Job_Code>
			<Location>Belfast</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
		</job>
		<job>
			<Category>Retail and Consumer</Category>
			<StartingDate> </StartingDate>
			<Description>PwC and Salesforce   PwC is the ... Learn more here  www.pwc.com/uk/diversity</Description>
			<CountryCode>GB</CountryCode>
			<Job_URL>http://www.careersexperienced.pwc.co.uk/ShowJob/Id/870656/Manager-Salesforce-Solutions-Architect/</Job_URL>
			<Country>United Kingdom</Country>
			<Experience>All our people need to demonstrate the skills and behaviours ... and relationships.</Experience>
			<EndingDate> </EndingDate>
			<Customer_Job_Code>18843BR</Customer_Job_Code>
			<Location>London</Location>
			<Type>Full Time</Type>
			<SalaryRange> </SalaryRange>
			<Job_Title>Manager - Salesforce Solutions Architect</Job_Title>
		</job>
	</Jobs>
</root>"""
        stdout = StringIO()
        stderr = StringIO()
        with patch('sample.vacancies.management.commands.loadvacancies.open', mock_open(read_data=XML)):
            call_command('loadvacancies', 'pwc', stdout=stdout, stderr=stderr)
        stdout = stdout.getvalue().strip()
        stderr = stderr.getvalue().strip()
        self.assertIn("1 from 2", stdout)
        vacancy_cnt = Vacancy.objects.count()
        self.assertIn('{} from 2'.format(vacancy_cnt), stdout)
        soup = BeautifulSoup(XML, "html.parser")
        self.assertIn(str(soup.findAll('job')[0]), stderr)
