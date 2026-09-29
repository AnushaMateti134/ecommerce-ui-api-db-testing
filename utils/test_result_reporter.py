from pathlib import Path
from datetime import datetime

from openpyxl import load_workbook


# Excel workbook in project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "ecommerce_QA_master_test_cases.xlsx"

RESULTS = []

RUN_ID = datetime.now().strftime("RUN-%Y%m%d-%H%M%S")


TEST_CASE_MAP = {
    # Users API
    "tests/api/test_users_api.py::test_create_user": "TC-USER-001",
    "tests/api/test_users_api.py::test_get_nonexistent_user": "TC-USER-002",
    "tests/api/test_users_api.py::test_create_user_with_invalid_email": "TC-USER-003",
    "tests/api/test_users_api.py::test_create_user_missing_username": "TC-USER-004",
    "tests/api/test_users_api.py::test_create_user_with_duplicate_username": "TC-USER-005",

    # Products API
    "tests/api/test_products_api.py::test_create_product": "TC-PROD-001",
    "tests/api/test_products_api.py::test_get_existing_product": "TC-PROD-002",
    "tests/api/test_products_api.py::test_get_nonexistent_product": "TC-PROD-003",
    "tests/api/test_products_api.py::test_create_product_missing_name": "TC-PROD-004",
    "tests/api/test_products_api.py::test_create_product_missing_category": "TC-PROD-005",

    # Orders API
    "tests/api/test_orders_api.py::test_create_order": "TC-ORD-001",
    "tests/api/test_orders_api.py::test_get_existing_order": "TC-ORD-002",
    "tests/api/test_orders_api.py::test_get_nonexistent_order": "TC-ORD-003",
    "tests/api/test_orders_api.py::test_create_order_with_invalid_user": "TC-ORD-004",
    "tests/api/test_orders_api.py::test_create_order_with_invalid_product": "TC-ORD-005",

    # Order validation
    "tests/api/test_order_validation_api.py::test_create_order_with_zero_quantity": "TC-ORD-006",
    "tests/api/test_order_validation_api.py::test_create_order_with_empty_items": "TC-ORD-007",
    "tests/api/test_order_validation_api.py::test_create_order_with_negative_quantity": "TC-ORD-008",

    # Database
    "tests/db/test_users_db.py::test_created_user_exists_in_database": "TC-DB-001",
    "tests/db/test_products_db.py::test_created_product_exists_in_database": "TC-DB-002",
    "tests/db/test_orders_db.py::test_created_order_exists_in_database": "TC-DB-003",

    # UI
    "tests/ui/test_login_ui.py::test_login_page_loads": "TC-UI-001",
    "tests/ui/test_products_ui.py::test_products_page_displays_products": "TC-UI-002",
    "tests/ui/test_cart_ui.py::test_add_product_to_cart": "TC-UI-003",
    "tests/ui/test_checkout_ui.py::test_place_order_from_ui": "TC-UI-004",
    "tests/ui/test_empty_cart_ui.py::test_empty_cart_cannot_checkout": "TC-UI-005",

    # E2E
    "tests/e2e/test_complete_purchase_flow.py::test_complete_purchase_flow": "TC-E2E-001",
}


def normalize_nodeid(nodeid):
    """Remove pytest parameter values such as [chromium]."""
    return nodeid.split("[", 1)[0]


def update_execution_result(
    test_case_id,
    status,
    duration=0,
    error="",
):
    """
    Update latest execution result in Test Cases sheet.
    """

    if not EXCEL_FILE.exists():
        print(f"WARNING: Excel file not found: {EXCEL_FILE}")
        return

    workbook = load_workbook(EXCEL_FILE)

    if "Test Cases" not in workbook.sheetnames:
        print("WARNING: Test Cases sheet not found.")
        return

    worksheet = workbook["Test Cases"]

    headers = {
        cell.value: cell.column
        for cell in worksheet[1]
    }

    test_case_column = headers.get("Test Case ID")
    status_column = headers.get("Execution Status")
    remarks_column = headers.get("Remarks")

    if not test_case_column or not status_column:
        print("WARNING: Required Excel columns not found.")
        return

    for row in range(2, worksheet.max_row + 1):

        current_id = worksheet.cell(
            row=row,
            column=test_case_column
        ).value

        if current_id == test_case_id:

            worksheet.cell(
                row=row,
                column=status_column
            ).value = status

            if remarks_column:

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                remarks = (
                    f"Last Run: {timestamp} | "
                    f"Duration: {duration:.2f}s"
                )

                if error:
                    remarks += f" | Error: {error[:1000]}"

                worksheet.cell(
                    row=row,
                    column=remarks_column
                ).value = remarks

            break

    workbook.save(EXCEL_FILE)


def pytest_runtest_logreport(report):
    """
    Capture the result of the actual test call.
    """

    if report.when != "call":
        return

    nodeid = normalize_nodeid(report.nodeid)

    test_case_id = TEST_CASE_MAP.get(
        nodeid,
        "UNMAPPED"
    )

    status = report.outcome.capitalize()

    error = ""

    if report.failed:
        error = str(report.longrepr)

    result = {
        "test_case_id": test_case_id,
        "nodeid": nodeid,
        "status": status,
        "duration": report.duration,
        "error": error,
    }

    RESULTS.append(result)

    print(
        f"\n[QA REPORTER] "
        f"{test_case_id} -> {status}"
    )


def pytest_sessionfinish(session, exitstatus):
    """
    Write all captured results to Excel at the end of the run.
    """

    print("\n")
    print("=" * 60)
    print("QA EXCEL REPORTER")
    print("=" * 60)

    if not RESULTS:
        print("No test results were captured.")
        print("=" * 60)
        return

    if not EXCEL_FILE.exists():
        print(f"Excel file not found: {EXCEL_FILE}")
        print("=" * 60)
        return

    workbook = load_workbook(EXCEL_FILE)

    # ---------------------------------------------------------
    # Execution Results sheet
    # ---------------------------------------------------------

    if "Execution Results" not in workbook.sheetnames:

        results_sheet = workbook.create_sheet(
            "Execution Results"
        )

        results_sheet.append([
            "Run ID",
            "Execution Date",
            "Execution Time",
            "Test Case ID",
            "Test Name",
            "Node ID",
            "Status",
            "Duration (sec)",
            "Error",
        ])

    else:

        results_sheet = workbook[
            "Execution Results"
        ]

    now = datetime.now()

    for result in RESULTS:

        test_name = result["nodeid"].split("::")[-1]

        results_sheet.append([
            RUN_ID,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            result["test_case_id"],
            test_name,
            result["nodeid"],
            result["status"],
            round(result["duration"], 2),
            result["error"],
        ])

    # ---------------------------------------------------------
    # Run History sheet
    # ---------------------------------------------------------

    if "Run History" not in workbook.sheetnames:

        history_sheet = workbook.create_sheet(
            "Run History"
        )

        history_sheet.append([
            "Run ID",
            "Execution Date",
            "Execution Time",
            "Total Tests",
            "Passed",
            "Failed",
            "Skipped",
            "Pytest Exit Status",
        ])

    else:

        history_sheet = workbook[
            "Run History"
        ]

    total = len(RESULTS)

    passed = sum(
        1
        for result in RESULTS
        if result["status"] == "Passed"
    )

    failed = sum(
        1
        for result in RESULTS
        if result["status"] == "Failed"
    )

    skipped = sum(
        1
        for result in RESULTS
        if result["status"] == "Skipped"
    )

    history_sheet.append([
        RUN_ID,
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        total,
        passed,
        failed,
        skipped,
        int(exitstatus),
    ])

    # ---------------------------------------------------------
    # Update latest status in Test Cases
    # ---------------------------------------------------------

    for result in RESULTS:

        if result["test_case_id"] == "UNMAPPED":
            continue

        update_execution_result(
            test_case_id=result["test_case_id"],
            status=result["status"],
            duration=result["duration"],
            error=result["error"],
        )

    workbook.save(EXCEL_FILE)

    print(f"Run ID: {RUN_ID}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Excel: {EXCEL_FILE}")
    print("=" * 60)