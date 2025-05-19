A fully asynchronous, zero-auth toolkit for Reddit data analysis
================================================================

.. raw:: html

   <p align="center"><strong>Knew Karma</strong> (/nuː ‘kɑːrmə/) is a fully asynchronous, zero-auth toolkit for Reddit data analysis designed to provide an extensive range of functionalities for exploring and analysing Reddit data. It includes a <strong>Command-Line Interface</strong> (<strong>CLI</strong>), and an <strong>Application Programming Interface</strong> (<strong>API</strong>) to enable easy integration in other Python projects and/or scripts.</p>

.. raw:: html

   <p align="center">
      <a href="https://github.com/knewkarma-io/knewkarma"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000?logo=github&link=https%3A%2F%2Fgithub.com%2Frly0nheart%2Fknewkarma"></a>
      <a href="https://pepy.tech/project/knewkarma"><img alt="Downloads" src="https://img.shields.io/pepy/dt/knewkarma?logo=pypi"></a>
      <a href="https://pypi.org/project/knewkarma"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/knewkarma?logo=pypi&link=https%3A%2F%2Fpypi.org%2Fproject%2Fknewkarma"></a>
      <a href="https://snapcraft.io/knewkarma"><img alt="Snap Version" src="https://img.shields.io/snapcraft/v/knewkarma/latest/stable?logo=snapcraft&color=%23BB431A"></a>
      <!--<a href="https://opencollective.com/knewkarma"><img alt="Open Collective backers and sponsors" src="https://img.shields.io/opencollective/all/knewkarma?logo=open-collective"></a>-->
   </p>

.. list-table:: Knew Karma provides detailed access to Reddit data across various categories [see table below]
   :widths: 25 25 50
   :header-rows: 1

   * - Category
     - Feature
     - Description
   * - **Post**
     - ``Data``
     - Retrieves an individual post's data.
   * -
     - ``Comments``
     - Retrieves an individual post's comments.
   * - **Posts**
     - ``New``
     - Retrieves new posts.
   * -
     - ``Reddit Front-Page``
     - Retrieves front-page posts.
   * -
     - ``Listing``
     - Retrieves posts from specified Reddit listings.
   * - **Search**
     - ``Users``
     - Searches for users.
   * -
     - ``Subreddits``
     - Searches for subreddits.
   * -
     - ``Posts``
     - Searches for posts.
   * - **Subreddit**
     - ``Profile``
     - Retrieves subreddit profile information.
   * -
     - ``Comments``
     - Retrieves comments from a subreddit.
   * -
     - ``Posts``
     - Retrieves posts from a subreddit.
   * -
     - ``Search Posts``
     - Returns a subreddit's posts that contain the specified keyword.
   * -
     - ``Wiki Pages``
     - Lists wiki pages in a subreddit.
   * -
     - ``Wiki Page``
     - Retrieves content from specific wiki pages.
   * - **Subreddits**
     - ``All``
     - Retrieves all subreddits.
   * -
     - ``Default``
     - Retrieves default subreddits.
   * -
     - ``New``
     - Retrieves new subreddits.
   * -
     - ``Popular``
     - Retrieves popular subreddits.
   * - **User**
     - ``Profile``
     - Retrieves user profile information.
   * -
     - ``Posts``
     - Retrieves user posts.
   * -
     - ``Comments``
     - Retrieves user comments.
   * -
     - ``Overview``
     - Retrieves user's most recent comment activity.
   * -
     - ``Search Posts``
     - Returns a user's posts that match with the specified search query.
   * -
     - ``Search Comments``
     - Returns a user's comments that match with the specified search query.
   * -
     - ``Top n Subreddits``
     - Identifies top subreddits based on user activity.
   * -
     - ``Moderated Subreddits``
     - Lists subreddits moderated by the user.
   * - **Users**
     - ``All``
     - Retrieves all users.
   * -
     - ``New``
     - Retrieves new users.
   * -
     - ``Popular``
     - Retrieves popular users.
