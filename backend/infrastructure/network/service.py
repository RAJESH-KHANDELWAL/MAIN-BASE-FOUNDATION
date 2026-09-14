    def list(
        self,
        status: Optional[str] = None,
        network_type: Optional[str] = None,
    ) -> List[NetworkInfo]:

        conditions = []
        values = []

        if status:
            conditions.append("status = ?")
            values.append(status)

        if network_type:
            if network_type not in self.ALLOWED_NETWORK_TYPES:
                raise ValueError(
                    f"Unsupported network type: "
                    f"{network_type}"
                )

            conditions.append("network_type = ?")
            values.append(network_type)

        if conditions:
            where_clause = (
                "WHERE " + " AND ".join(conditions)
            )
        else:
            where_clause = ""

        rows = self.database.fetchall(
            f"""
            SELECT *
            FROM {self.TABLE_NAME}
            {where_clause}
            ORDER BY rowid ASC
            """,
            values,
        )

        return [
            self._to_model(row)
            for row in rows
        ]
