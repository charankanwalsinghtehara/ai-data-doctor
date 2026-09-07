const API_BASE = "/api";


// =========================================================
// SECTION NAVIGATION
// =========================================================

function showSection(sectionId) {

    document
        .querySelectorAll(".content-section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


    const selectedSection =
        document.getElementById(sectionId);


    if (selectedSection) {

        selectedSection.classList.add(
            "active-section"
        );

    }


    document
        .querySelectorAll(".nav-btn")
        .forEach(button => {

            button.classList.remove("active");

        });


    const activeButton =
        document.querySelector(
            `[data-section="${sectionId}"]`
        );


    if (activeButton) {

        activeButton.classList.add("active");

    }


    const titles = {

        dashboard: "Dashboard",

        upload: "Upload Dataset",

        datasets: "My Datasets",

        analysis: "Data Analysis",

        cleaning: "Data Cleaning",

        visualization: "Visualizations",

        ml: "Machine Learning",

        history: "Analysis History"

    };


    document.getElementById(
        "pageTitle"
    ).textContent =
        titles[sectionId] || "AI Data Doctor";


    // Load datasets when required

    if (
        sectionId === "datasets" ||
        sectionId === "analysis" ||
        sectionId === "cleaning" ||
        sectionId === "visualization" ||
        sectionId === "ml" ||
        sectionId === "history"
    ) {

        loadDatasets();

    }

}


// =========================================================
// SIDEBAR EVENTS
// =========================================================

document
    .querySelectorAll(".nav-btn")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                showSection(
                    button.dataset.section
                );

            }
        );

    });


// =========================================================
// LOAD DATASETS
// =========================================================

async function loadDatasets() {

    const container =
        document.getElementById(
            "datasetsList"
        );


    if (container) {

        container.innerHTML =
            "<p>Loading datasets...</p>";

    }


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/`
            );


        if (!response.ok) {

            throw new Error(
                "Could not load datasets."
            );

        }


        const datasets =
            await response.json();


        const datasetCount =
            document.getElementById(
                "datasetCount"
            );


        if (datasetCount) {

            datasetCount.textContent =
                datasets.length;

        }


        updateDatasetSelects(datasets);


        if (!container) {

            return;

        }


        if (datasets.length === 0) {

            container.innerHTML = `

                <div class="alert alert-info">

                    No datasets uploaded yet.

                </div>

            `;

            return;

        }


        container.innerHTML = "";


        datasets.forEach(dataset => {

            const card =
                document.createElement("div");


            card.className =
                "dataset-card";


            const uploadedDate =
                dataset.uploaded_at
                    ?
                    new Date(
                        dataset.uploaded_at
                    ).toLocaleString()
                    :
                    "Unknown";


            card.innerHTML = `

                <div class="d-flex justify-content-between align-items-center">

                    <div>

                        <h5>

                            📄 ${dataset.name}

                        </h5>


                        <p class="mb-1">

                            <strong>File Size:</strong>

                            ${dataset.file_size || 0} bytes

                        </p>


                        <p class="mb-0">

                            <strong>Uploaded:</strong>

                            ${uploadedDate}

                        </p>

                    </div>


                    <div>

                        <button
                            class="btn btn-primary btn-sm"
                            onclick="selectDataset(${dataset.id})"
                        >

                            Use Dataset

                        </button>

                    </div>

                </div>

            `;


            container.appendChild(card);

        });

    }

    catch (error) {

        if (container) {

            container.innerHTML = `

                <div class="alert alert-danger">

                    Could not load datasets.

                </div>

            `;

        }


        console.error(error);

    }

}


// =========================================================
// UPDATE ALL DATASET SELECT DROPDOWNS
// =========================================================

function updateDatasetSelects(datasets) {

    const selectIds = [

        "analysisDataset",

        "cleaningDataset",

        "visualizationDataset",

        "mlDataset",

        "historyDataset"

    ];


    selectIds.forEach(id => {

        const select =
            document.getElementById(id);


        if (!select) {

            return;

        }


        const currentValue =
            select.value;


        select.innerHTML = `

            <option value="">

                Select Dataset

            </option>

        `;


        datasets.forEach(dataset => {

            const option =
                document.createElement("option");


            option.value =
                dataset.id;


            option.textContent =
                dataset.name;


            select.appendChild(option);

        });


        if (currentValue) {

            select.value =
                currentValue;

        }

    });

}


// =========================================================
// SELECT DATASET
// =========================================================

function selectDataset(datasetId) {

    document
        .querySelectorAll("select")
        .forEach(select => {

            const option =
                select.querySelector(
                    `option[value="${datasetId}"]`
                );


            if (option) {

                select.value =
                    datasetId;

            }

        });


    showSection("analysis");

}


// =========================================================
// FILE SELECTION
// =========================================================

const datasetFileInput =
    document.getElementById(
        "datasetFile"
    );


if (datasetFileInput) {

    datasetFileInput.addEventListener(
        "change",
        function() {

            const selected =
                document.getElementById(
                    "selectedFile"
                );


            if (
                this.files.length > 0 &&
                selected
            ) {

                selected.textContent =
                    this.files[0].name;

            }

        }
    );

}


// =========================================================
// UPLOAD DATASET
// =========================================================

const uploadForm =
    document.getElementById(
        "uploadForm"
    );


if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const fileInput =
                document.getElementById(
                    "datasetFile"
                );


            const message =
                document.getElementById(
                    "uploadMessage"
                );


            if (!fileInput.files.length) {

                message.innerHTML = `

                    <div class="alert alert-warning">

                        Please select a dataset file.

                    </div>

                `;

                return;

            }


            const formData =
                new FormData();


            formData.append(
                "file",
                fileInput.files[0]
            );


            message.innerHTML = `

                <p>

                    Uploading dataset...

                </p>

            `;


            try {

                const response =
                    await fetch(
                        `${API_BASE}/datasets/`,
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        JSON.stringify(data)
                    );

                }


                message.innerHTML = `

                    <div class="alert alert-success">

                        ✅ Dataset uploaded successfully!

                    </div>

                `;


                fileInput.value = "";


                const selected =
                    document.getElementById(
                        "selectedFile"
                    );


                if (selected) {

                    selected.textContent =
                        "Choose your dataset";

                }


                await loadDatasets();

            }

            catch (error) {

                message.innerHTML = `

                    <div class="alert alert-danger">

                        ❌ Upload failed.

                    </div>

                `;


                console.error(error);

            }

        }
    );

}


// =========================================================
// COMPLETE DATASET ANALYSIS
// =========================================================

async function analyzeDataset() {

    const datasetId =
        document.getElementById(
            "analysisDataset"
        ).value;


    const result =
        document.getElementById(
            "analysisResult"
        );


    if (!datasetId) {

        result.innerHTML = `

            <div class="alert alert-warning">

                Please select a dataset.

            </div>

        `;

        return;

    }


    result.innerHTML = `

        <p>

            🔍 Analyzing dataset...

        </p>

    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/${datasetId}/analysis/`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.details ||
                "Analysis failed"
            );

        }


        const analysis =
            data.analysis;


        const recommendations =
            analysis.cleaning_recommendations || [];


        const insights =
            analysis.insights || [];


        result.innerHTML = `

            <div class="row">


                <div class="col-md-4">

                    <div class="stat-card">

                        <h3>

                            ${analysis.dataset_overview.rows}

                        </h3>

                        <p>

                            Rows

                        </p>

                    </div>

                </div>



                <div class="col-md-4">

                    <div class="stat-card">

                        <h3>

                            ${analysis.dataset_overview.columns}

                        </h3>

                        <p>

                            Columns

                        </p>

                    </div>

                </div>



                <div class="col-md-4">

                    <div class="stat-card">

                        <h3>

                            ${analysis.data_quality.score}

                        </h3>

                        <p>

                            Quality Score

                            (${analysis.data_quality.grade})

                        </p>

                    </div>

                </div>


            </div>



            <div class="mt-4">

                <h4>

                    💡 Dataset Insights

                </h4>


                <ul>

                    ${insights
                        .map(
                            insight =>
                                `<li>${insight}</li>`
                        )
                        .join("")
                    }

                </ul>

            </div>



            <div class="mt-4">

                <h4>

                    🧹 Cleaning Recommendations

                </h4>


                ${

                    recommendations.length > 0

                    ?

                    `

                    <ul>

                        ${recommendations
                            .map(
                                item => `

                                    <li>

                                        <strong>

                                            ${item.issue}

                                        </strong>

                                        ${

                                            item.column

                                            ?

                                            `(${item.column})`

                                            :

                                            ""

                                        }

                                        :

                                        ${item.recommendation}

                                    </li>

                                `
                            )
                            .join("")
                        }

                    </ul>

                    `

                    :

                    `

                    <p>

                        No major cleaning recommendations.

                    </p>

                    `

                }

            </div>

        `;


        const analysisCount =
            document.getElementById(
                "analysisCount"
            );


        if (analysisCount) {

            const currentCount =
                parseInt(
                    analysisCount.textContent
                ) || 0;


            analysisCount.textContent =
                currentCount + 1;

        }

    }

    catch (error) {

        result.innerHTML = `

            <div class="alert alert-danger">

                ❌ ${error.message}

            </div>

        `;

    }

}


// =========================================================
// AUTOMATIC DATA CLEANING
// =========================================================

async function cleanDataset() {

    const datasetId =
        document.getElementById(
            "cleaningDataset"
        ).value;


    const result =
        document.getElementById(
            "cleaningResult"
        );


    if (!datasetId) {

        result.innerHTML = `

            <div class="alert alert-warning">

                Please select a dataset.

            </div>

        `;

        return;

    }


    result.innerHTML = `

        <p>

            🧹 Cleaning dataset...

        </p>

    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/${datasetId}/clean/`,
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.details ||
                "Cleaning failed"
            );

        }


        const summary =
            data.cleaning_summary;


        const actions =
            summary.actions || [];


        result.innerHTML = `

            <div class="alert alert-success">

                ✅ ${data.message}

            </div>



            <h4>

                Cleaning Summary

            </h4>


            <div class="row mt-3">


                <div class="col-md-3">

                    <div class="stat-card">

                        <h3>

                            ${summary.original_rows}

                        </h3>

                        <p>

                            Original Rows

                        </p>

                    </div>

                </div>



                <div class="col-md-3">

                    <div class="stat-card">

                        <h3>

                            ${summary.cleaned_rows}

                        </h3>

                        <p>

                            Cleaned Rows

                        </p>

                    </div>

                </div>



                <div class="col-md-3">

                    <div class="stat-card">

                        <h3>

                            ${summary.original_columns}

                        </h3>

                        <p>

                            Original Columns

                        </p>

                    </div>

                </div>



                <div class="col-md-3">

                    <div class="stat-card">

                        <h3>

                            ${summary.cleaned_columns}

                        </h3>

                        <p>

                            Cleaned Columns

                        </p>

                    </div>

                </div>


            </div>



            <div class="mt-4">

                <h4>

                    Actions Performed

                </h4>


                <ul>

                    ${

                        actions.length > 0

                        ?

                        actions
                            .map(
                                action =>

                                    `<li>${action.action}</li>`
                            )
                            .join("")

                        :

                        "<li>No cleaning actions were required.</li>"

                    }

                </ul>

            </div>



            <a
                href="${data.cleaned_file}"
                class="btn btn-success mt-3"
                target="_blank"
            >

                ⬇ Download Cleaned Dataset

            </a>

        `;

    }

    catch (error) {

        result.innerHTML = `

            <div class="alert alert-danger">

                ❌ ${error.message}

            </div>

        `;

    }

}


// =========================================================
// VISUALIZATION
// =========================================================

async function generateVisualization(chartType) {

    const datasetId =
        document.getElementById(
            "visualizationDataset"
        ).value;


    const result =
        document.getElementById(
            "visualizationResult"
        );


    if (!datasetId) {

        result.innerHTML = `

            <div class="alert alert-warning">

                Please select a dataset first.

            </div>

        `;

        return;

    }


    result.innerHTML = `

        <p>

            📈 Generating visualization...

        </p>

    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/${datasetId}/visualization/${chartType}/`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.details ||
                data.error ||
                "Visualization failed"
            );

        }


        const imageUrl =
            data.image ||
            data.visualization ||
            data.chart_url ||
            data.file;


        if (!imageUrl) {

            throw new Error(
                "Visualization image was not returned by the backend."
            );

        }


        result.innerHTML = `

            <div class="card p-3">

                <h4>

                    ${chartType
                        .replace(
                            /(^\w|\s\w)/g,
                            letter =>
                                letter.toUpperCase()
                        )
                    }

                </h4>


                <img
                    src="${imageUrl}"
                    class="img-fluid mt-3"
                    alt="Dataset Visualization"
                >

            </div>

        `;

    }

    catch (error) {

        result.innerHTML = `

            <div class="alert alert-danger">

                ❌ ${error.message}

            </div>

        `;


        console.error(error);

    }

}


// =========================================================
// MACHINE LEARNING
// =========================================================

async function trainModel(modelType) {

    const datasetId =
        document.getElementById(
            "mlDataset"
        ).value;


    const targetColumn =
        document.getElementById(
            "targetColumn"
        ).value
        .trim();


    const result =
        document.getElementById(
            "mlResult"
        );


    if (!datasetId) {

        result.innerHTML = `

            <div class="alert alert-warning">

                Please select a dataset.

            </div>

        `;

        return;

    }


    if (!targetColumn) {

        result.innerHTML = `

            <div class="alert alert-warning">

                Please enter the target column name.

            </div>

        `;

        return;

    }


    result.innerHTML = `

        <p>

            🤖 Training ${modelType} model...

        </p>

    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/${datasetId}/ml/${modelType}/`,
                {
                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            target_column:
                                targetColumn

                        })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.details ||
                data.error ||
                "Machine learning failed"
            );

        }


        result.innerHTML = `

            <div class="alert alert-success">

                ✅ Machine Learning model trained successfully!

            </div>


            <div class="card p-3 mt-3">

                <h4>

                    🤖 Model Results

                </h4>


                <pre class="mt-3">

${JSON.stringify(data, null, 2)}

                </pre>

            </div>

        `;

    }

    catch (error) {

        result.innerHTML = `

            <div class="alert alert-danger">

                ❌ ${error.message}

            </div>

        `;


        console.error(error);

    }

}


// =========================================================
// ANALYSIS HISTORY
// =========================================================

async function loadHistory() {

    const datasetId =
        document.getElementById(
            "historyDataset"
        ).value;


    const result =
        document.getElementById(
            "historyResult"
        );


    if (!datasetId) {

        result.innerHTML = `

            Select a dataset to view history.

        `;

        return;

    }


    result.innerHTML = `

        <p>

            Loading analysis history...

        </p>

    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/datasets/${datasetId}/history/`
            );


        const history =
            await response.json();


        if (!response.ok) {

            throw new Error(
                "Could not load history."
            );

        }


        if (!history.length) {

            result.innerHTML = `

                <div class="alert alert-info">

                    No analysis history found for this dataset.

                </div>

            `;

            return;

        }


        result.innerHTML = "";


        history.forEach(item => {

            const card =
                document.createElement("div");


            card.className =
                "dataset-card";


            const createdAt =
                item.created_at

                ?

                new Date(
                    item.created_at
                ).toLocaleString()

                :

                "Unknown";


            card.innerHTML = `

                <h5>

                    Analysis #${item.id}

                </h5>


                <p>

                    <strong>Date:</strong>

                    ${createdAt}

                </p>


                <details>

                    <summary>

                        View Analysis Result

                    </summary>


                    <pre class="mt-3">

${JSON.stringify(
    item.analysis_result,
    null,
    2
)}

                    </pre>

                </details>

            `;


            result.appendChild(card);

        });

    }

    catch (error) {

        result.innerHTML = `

            <div class="alert alert-danger">

                ❌ ${error.message}

            </div>

        `;


        console.error(error);

    }

}


// =========================================================
// INITIAL LOAD
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadDatasets();

    }
);