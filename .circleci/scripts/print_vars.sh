#!/usr/bin/env bash
set -e

function print_var {
  echo "$1: [${!1}]"
}

echo "########"
echo "Here's what's stored in CircleCI:"
echo "########"
print_var "FORM_API_URL_PROD"
print_var "DEPLOYMENT_BUCKET_OPO_PROD"
print_var "DEPLOYMENT_BUCKET_DAY_LABOR_PROD"
print_var "CI_PROD_API_OPO"
print_var "CI_PROD_BUCKET_OPO"
