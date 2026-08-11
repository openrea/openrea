// SPDX-License-Identifier: Apache-2.0
// openREA schema-only package. Canonical source: https://github.com/openrea/openrea
const schema = require("./openrea.schema.json");

module.exports = schema;
module.exports.SCHEMA = schema;
module.exports.SCHEMA_VERSION = schema.properties.openrea_version.const;
