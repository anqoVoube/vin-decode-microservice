from drf_yasg import openapi

response_schema_dict = {
    "200": openapi.Response(
        description="200 OK",
        examples={
            "application/json": {
                "vin": "SCBBR9ZA1AC063223",
                "year": "1997",
                "make": "Plymouth",
                "model": "Prowler",
                "type": "DOHC 48V TURBO",
                "color": "Yellow",
                "dimensions": {
                  "Wheelbase": "112.50",
                  "Rear Legroom": "39.50",
                  "Front Legroom": "41.20",
                },
                "weight": {
                  "type": "Curb Weight",
                  "unit": "lbs",
                  "value": 5568
                }
            }
        }
    ),
}

vin_id = openapi.Parameter(
    'id', openapi.IN_PATH,
    description="VIN itself",
    example="JN8DR07XX1W514175",
    type=openapi.TYPE_STRING
)
