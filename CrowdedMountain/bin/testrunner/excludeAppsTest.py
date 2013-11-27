#!/usr/bin/env python
from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

class ExcludeAppsTestSuiteRunner(DjangoTestSuiteRunner):
    """Override the default django 'test' command, exclude from testing
    apps which we know will fail."""

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not test_labels:
            # No appnames specified on the command line, so we run all
            # tests, but remove those which we know are troublesome.
            APPS_TO_NOT_RUN = (
                'django_extensions',
            )
            test_labels = [app for app in settings.INSTALLED_APPS
                            if not app in APPS_TO_NOT_RUN
                            and not app.startswith('django.')]
        return super(ExcludeAppsTestSuiteRunner, self).run_tests(
                                      test_labels, extra_tests, **kwargs)
