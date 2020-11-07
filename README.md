# Time series data for the cases of covid-19 in Mexico

The Mexican Ministry of Health (Secretaría de Salud) publishes an open dataset about cases of covid-19 through [its website](https://www.gob.mx/salud/documentos/datos-abiertos-152127). Each suspected case is recorded as a row in a massive table that grows daily in size and is hard to manipulate.

In this repo we store a summary of the dataset in the friendly form of time series for each of the 32 states and the total for the country.

We track some of the most useful variables, in particular number of *confirmed*, *negative* and *suspected cases*, number of *deaths* and number of *patients hospitalised* and *placed in intensive care*.

Our repo inherits the limitations of the original dataset, the most notable of which is the lack of information regarding the recovery of patients. As a result, all of the counts that we present in this repo are cumulative sums.

## Date of assignment of cases

The data published by the Ministry of Health comes with a significant delay due to a/ the intrinsic time it takes to get a test result and b/ the time it takes to enter the patient information into the records. A positive case confirmed today could be in fact the result of a test done two weeks ago. As a result, there are two possible ways to count a positive case:

1. We assign the case to the date when the patient visited a clinic (this information is published within the official database), which we assume is also the date when the test sample was taken.
2. We use the date when the result was included as a confirmed positive case in the official database.

For most countries, the only form of counting available is the second form and it is remarkable that the Mexican government published detailed information about individual cases. For the sake of comparison we include the second form of counting under [data/daily_totals](data/daily_totals), but we highlight the first form under [data](data) because we believe that it gives a more accurate reflection of the evolution of the pandemic in the presence of delays as large as two weeks


## Code and data source

Our code is made up of a couple of Python and bash scripts that are located under the directory [code](code).

Due to downloading restrictions for IP addresses that are not in Mexico, we download the official dataset using a mirror set-up by the National Autonomous University (UNAM).

**Note:** The original dataset contains incorrect UTF-8 encoding as explained (in Spanish) in the April 28 note [here](https://github.com/mexicovid19/Mexico-datos/#avisos). The maintainers of the UNAM mirror pre-process the official database on our behalf by running the Perl script [Encoding::FixLatin](https://metacpan.org/pod/Encoding::FixLatin) to convert any latin encoding to UTF-8.


## License

The official data is published with the License `Libre Uso MX`, as stated in the [open data website of the Mexican government](https://datos.gob.mx/busca/dataset/informacion-referente-a-casos-covid-19-en-mexico). Our code is made available with an MIT License.
