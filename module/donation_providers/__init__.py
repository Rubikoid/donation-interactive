from . import donation_alerts
from . import test_alerts

providers = {
    donation_alerts.DonationAlertsProvider.name: donation_alerts.DonationAlertsProvider,
    test_alerts.TestingProvider.name: test_alerts.TestingProvider,
}
