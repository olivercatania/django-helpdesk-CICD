from django.test import TestCase

from helpdesk.models import Queue, Ticket, TicketDependency


class TicketDependencyCIRegressionTests(TestCase):
    """Check how a ticket's dependency statuses affect resolution eligibility."""

    @classmethod
    def setUpTestData(cls):
        cls.queue = Queue.objects.create(title="CI test queue", slug="ci-test")
        cls.ticket = Ticket.objects.create(
            title="Primary issue",
            submitter_email="primary@example.com",
            queue=cls.queue,
        )

    def _make_blocker(self, status, title="Dependent issue"):
        blocker = Ticket.objects.create(
            title=title,
            submitter_email="dependency@example.com",
            queue=self.queue,
            status=status,
        )
        TicketDependency.objects.create(ticket=self.ticket, depends_on=blocker)
        return blocker

    def test_ticket_without_dependencies_can_be_resolved(self):
        """No dependency should block the primary ticket."""
        self.assertTrue(self.ticket.can_be_resolved)

    def test_mixed_dependencies_still_block_resolution(self):
        """One open dependency must block even if another is resolved."""
        self._make_blocker(Ticket.RESOLVED_STATUS, "Resolved dependency")
        self._make_blocker(Ticket.REOPENED_STATUS, "Reopened dependency")

        self.assertFalse(self.ticket.can_be_resolved)

    def test_resolving_last_blocker_allows_resolution(self):
        """A ticket becomes resolvable after its last blocker is resolved."""
        blocker = self._make_blocker(Ticket.REOPENED_STATUS)
        self.assertFalse(self.ticket.can_be_resolved)

        blocker.status = Ticket.RESOLVED_STATUS
        blocker.save(update_fields=["status"])

        self.assertTrue(self.ticket.can_be_resolved)

    def test_reopening_dependency_blocks_resolution_again(self):
        """A previously resolved dependency can block its parent again."""
        blocker = self._make_blocker(Ticket.RESOLVED_STATUS)
        self.assertTrue(self.ticket.can_be_resolved)

        blocker.status = Ticket.REOPENED_STATUS
        blocker.save(update_fields=["status"])

        self.assertFalse(self.ticket.can_be_resolved)
