#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from desktop.lib.conf import Config, UnspecifiedConfigSection, ConfigSection


def zkensemble():
  """
  Try to guess the value if no values are specified.
  """
  try:
    # Backward compatibility until Hue 4
    from zookeeper.conf import CLUSTERS
    clusters = CLUSTERS.get()
    if clusters['default'].HOST_PORTS.get() != 'localhost:2181':
      return '%s/solr' % clusters['default'].HOST_PORTS.get()
  except:
    LOG.exception('failed to get zookeeper ensemble')

  try:
    from search.conf import SOLR_URL
    parsed = urlparse(SOLR_URL.get())
    return "%s:2181/solr" % (parsed.hostname or 'localhost')
  except:
    LOG.exception('failed to get solr url')

  return "localhost:2181"


CLUSTERS = UnspecifiedConfigSection(
  "clusters",
  help="One entry for each ZooKeeper cluster",
  each=ConfigSection(
    help="Information about a single ZooKeeper cluster",
    members=dict(
      ENSEMBLE=Config(
          "ensemble",
          help="ZooKeeper ensemble. Comma separated list of Host/Port, e.g. localhost:2181,localhost:2182,localhost:2183",
          dynamic_default=zkensemble,
          type=str,
      ),
      PRINCIPAL_NAME=Config(
          "principal_name",
          help="Name of Kerberos principal when using security",
          default="zookeeper",
          type=str,
      ),
    )
  )
)
