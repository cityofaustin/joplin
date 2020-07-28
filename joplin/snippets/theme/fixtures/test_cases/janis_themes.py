import os
from snippets.theme.fixtures.helpers.create_fixture import create_fixture


def permits_tickets():
    theme_data = {
        "slug": "permits-tickets",
        "text": "Permits and tickets",
        "text_es": "Permisos y multas",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def housing_utilities():
    theme_data = {
        "slug": "housing-utilities",
        "text": "Housing and utilities",
        "text_es": "Vivienda y servicios p\u00fablicos",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def pets():
    theme_data = {
        "slug": "pets",
        "text": "Pets",
        "text_es": "Mascotas",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def health_safety():
    theme_data = {
        "slug": "health-safety",
        "text": "Health and safety",
        "text_es": "Salud y seguridad",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def explore_visit():
    theme_data = {
        "slug": "explore-visit",
        "text": "Explore and visit",
        "text_es": "Explore y visite",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def government_business():
    theme_data = {
        "slug": "government-business",
        "text": "Government and business",
        "text_es": "Gobierno y negocios",
    }

    return create_fixture(theme_data, os.path.basename(__file__))


def jobs():
    theme_data = {
        "slug": "jobs",
        "text": "Jobs",
        "text_es": "Empleos",
    }

    return create_fixture(theme_data, os.path.basename(__file__))

