from . import donation_alerts
from . import test_alerts

providers = {
    "DonationAlertsProvider": donation_alerts.DonationAlertsProvider,
    "TestingProvider": test_alerts.TestingProvider,
}
