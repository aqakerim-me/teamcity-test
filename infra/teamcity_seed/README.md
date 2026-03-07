# TeamCity Seed

This directory stores the TeamCity server seed used for both CI and local startup.

Refresh the seed only from a cleanly stopped local TeamCity datadir after these steps are complete:

1. Submit the License Agreement.
2. Create the `admin/admin` account.
3. Create an access token in the admin profile.
4. Copy that token into [resources/config.properties](C:/git/teamcity-test/resources/config.properties) as `admin.bearerToken`.

The refreshed seed is valid only when the token in TeamCity, `resources/config.properties`, and `secrets.TC_ADMIN_BEARERTOKEN` all match.

Default startup and teardown now use the same seeded TeamCity baseline everywhere:

- `scripts/start_infra.sh` restores this seed into a disposable runtime and starts TeamCity from that prepared state.
- `scripts/stop_infra.sh` removes the disposable runtime and Docker volumes by default.
- Local development and CI both use the same no-argument flow: `bash scripts/start_infra.sh` and `bash scripts/stop_infra.sh`.
- The single `infra/docker_compose/docker-compose.yml` file assumes those runtime bind-mount paths have been prepared by the seed restore step.
- Use `scripts/stop_infra.sh --preserve-volumes` only when you intentionally want to keep Docker volumes around for debugging.
