MATCH (a {asset_id: $asset_id})-[:PRODUCES|TRANSFORMS*1..4]->(downstream)
RETURN downstream.asset_id AS asset_id

